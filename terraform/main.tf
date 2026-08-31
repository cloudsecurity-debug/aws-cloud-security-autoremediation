terraform {
  required_version = ">= 1.13.0"

  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region = "eu-north-1"
}

resource "aws_s3_bucket" "security_test" {
  bucket_prefix = "cloud-security-test-"

  tags = {
    Project = var.project_name
    Purpose = "security-autoremediation-test"
  }
}

resource "aws_s3_bucket_public_access_block" "security_test" {
  bucket = aws_s3_bucket.security_test.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "security_test" {
  bucket = aws_s3_bucket.security_test.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "security_test" {
  bucket = aws_s3_bucket.security_test.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
