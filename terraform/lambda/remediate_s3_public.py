import json
import boto3

s3 = boto3.client("s3")


def lambda_handler(event, context):
    print(json.dumps(event))

    bucket_name = event.get("bucket_name")

    if not bucket_name:
        detail = event.get("detail", {})
        bucket_name = detail.get("resourceId")

    if not bucket_name:
        raise ValueError("Missing S3 bucket name")

    s3.put_public_access_block(
        Bucket=bucket_name,
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": True,
            "IgnorePublicAcls": True,
            "BlockPublicPolicy": True,
            "RestrictPublicBuckets": True,
        },
    )

    return {
        "statusCode": 200,
        "bucket": bucket_name,
        "action": "public_access_block_enforced",
    }
