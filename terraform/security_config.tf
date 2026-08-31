# AWS Config resources will be defined here.
# Detection rules are intentionally separated from core infrastructure.

resource "aws_s3_bucket" "config" {
  bucket_prefix = "cloud-security-config-"

  tags = {
    Project = var.project_name
    Purpose = "aws-config-delivery"
  }
}

resource "aws_s3_bucket_public_access_block" "config" {
  bucket = aws_s3_bucket.config.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "config" {
  bucket = aws_s3_bucket.config.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_iam_role" "config" {
  name = "${var.project_name}-config"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "config.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Project = var.project_name
    Purpose = "aws-config"
  }
}

resource "aws_iam_role_policy_attachment" "config" {
  role       = aws_iam_role.config.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWS_ConfigRole"
}

data "aws_caller_identity" "current" {}

resource "aws_s3_bucket_policy" "config" {
  bucket = aws_s3_bucket.config.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AWSConfigBucketPermissionsCheck"
        Effect = "Allow"
        Principal = {
          Service = "config.amazonaws.com"
        }
        Action   = "s3:GetBucketAcl"
        Resource = aws_s3_bucket.config.arn
      },
      {
        Sid    = "AWSConfigBucketDeliveryList"
        Effect = "Allow"
        Principal = {
          Service = "config.amazonaws.com"
        }
        Action   = "s3:ListBucket"
        Resource = aws_s3_bucket.config.arn
      },
      {
        Sid    = "AWSConfigBucketDelivery"
        Effect = "Allow"
        Principal = {
          Service = "config.amazonaws.com"
        }
        Action   = "s3:PutObject"
        Resource = "${aws_s3_bucket.config.arn}/AWSLogs/${data.aws_caller_identity.current.account_id}/*"
        Condition = {
          StringEquals = {
            "s3:x-amz-acl" = "bucket-owner-full-control"
          }
        }
      }
    ]
  })
}

resource "aws_config_configuration_recorder" "main" {
  name     = "${var.project_name}-recorder"
  role_arn = aws_iam_role.config.arn

  recording_group {
    all_supported                 = true
    include_global_resource_types = true
  }
}

resource "aws_config_delivery_channel" "main" {
  name           = "${var.project_name}-channel"
  s3_bucket_name = aws_s3_bucket.config.id

  depends_on = [
    aws_s3_bucket_policy.config
  ]
}

resource "aws_config_configuration_recorder_status" "main" {
  name       = aws_config_configuration_recorder.main.name
  is_enabled = true

  depends_on = [
    aws_config_delivery_channel.main
  ]
}

resource "aws_config_config_rule" "s3_public_read_prohibited" {
  name        = "${var.project_name}-s3-public-read-prohibited"
  description = "Detects S3 buckets that allow public read access."

  source {
    owner             = "AWS"
    source_identifier = "S3_BUCKET_PUBLIC_READ_PROHIBITED"
  }

  depends_on = [
    aws_config_configuration_recorder_status.main
  ]
}

resource "aws_iam_role" "remediation_lambda" {
  name = "${var.project_name}-remediation-lambda"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Project = var.project_name
    Purpose = "security-remediation"
  }
}

resource "aws_iam_role_policy" "remediation_lambda" {
  name = "${var.project_name}-remediation-policy"
  role = aws_iam_role.remediation_lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "CloudWatchLogs"
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:*"
      },
      {
        Sid    = "EnforceS3PublicAccessBlock"
        Effect = "Allow"
        Action = [
          "s3:GetBucketPublicAccessBlock",
          "s3:PutBucketPublicAccessBlock"
        ]
        Resource = "arn:aws:s3:::*"
      }
    ]
  })
}

resource "aws_lambda_function" "remediation" {
  function_name = "${var.project_name}-remediation"

  filename         = "${path.module}/remediate_s3_public.zip"
  source_code_hash = filebase64sha256("${path.module}/remediate_s3_public.zip")

  role    = aws_iam_role.remediation_lambda.arn
  handler = "remediate_s3_public.lambda_handler"
  runtime = "python3.12"

  timeout = 30

  tags = {
    Project = var.project_name
    Purpose = "security-remediation"
  }

  depends_on = [
    aws_iam_role_policy.remediation_lambda
  ]
}

resource "aws_lambda_permission" "config" {
  statement_id  = "AllowAWSConfigInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.remediation.function_name
  principal     = "config.amazonaws.com"
}


resource "aws_cloudwatch_event_rule" "config_noncompliant" {
  name        = "${var.project_name}-config-noncompliant"
  description = "Triggers remediation when AWS Config detects an S3 compliance violation."

  event_pattern = jsonencode({
    source = [
      "aws.config"
    ]
    detail-type = [
      "Config Rules Compliance Change"
    ]
    detail = {
      configRuleName = [
        aws_config_config_rule.s3_public_read_prohibited.name
      ]
      newEvaluationResult = {
        complianceType = [
          "NON_COMPLIANT"
        ]
      }
    }
  })
}

resource "aws_cloudwatch_event_target" "config_remediation" {
  rule = aws_cloudwatch_event_rule.config_noncompliant.name
  arn  = aws_lambda_function.remediation.arn

  input_transformer {
    input_paths = {
      bucket_name = "$.detail.resourceId"
    }

    input_template = <<EOF
{"bucket_name": <bucket_name>}
EOF
  }
}

resource "aws_lambda_permission" "eventbridge" {
  statement_id  = "AllowEventBridgeInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.remediation.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.config_noncompliant.arn
}
