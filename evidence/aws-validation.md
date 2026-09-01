# AWS Deployment Validation

## Project

AWS Cloud Security Auto-Remediation

## Region

`eu-north-1`

## Lambda Validation

Function: `cloud-security-autoremediation-remediation`

- Runtime: `Python 3.12`
- Deployment verified in AWS Lambda
- Remediation function is connected to the production EventBridge rule

## AWS Config Validation

Rule: `cloud-security-autoremediation-s3-public-read-prohibited`

- State: `ACTIVE`
- Source identifier: `S3_BUCKET_PUBLIC_READ_PROHIBITED`
- Evaluation mode: `DETECTIVE`
- AWS Config recorder: active
- Recorder status: `SUCCESS`

## EventBridge Validation

Rule: `cloud-security-autoremediation-config-noncompliant`

- State: `ENABLED`
- Event source: `aws.config`
- Compliance type filter: `NON_COMPLIANT`
- Config rule: `cloud-security-autoremediation-s3-public-read-prohibited`

## EventBridge Target

The production EventBridge rule was verified with one target pointing to:

`cloud-security-autoremediation-remediation`

The target is the deployed remediation Lambda.

## Live End-to-End Validation

A controlled test was performed against the dedicated security-test S3 bucket.

The test introduced a temporary public-read bucket policy to create a controlled AWS Config compliance violation.

AWS Config recorded the resource as:

`NON_COMPLIANT`

The compliance history subsequently recorded the resource as:

`COMPLIANT`

The history contained repeated `NON_COMPLIANT` and `COMPLIANT` evaluations for the test bucket, demonstrating that the control was evaluated and returned to compliance.

## S3 Remediation Validation

After remediation, the bucket's Public Access Block configuration was verified as:

- `BlockPublicAcls: true`
- `IgnorePublicAcls: true`
- `BlockPublicPolicy: true`
- `RestrictPublicBuckets: true`

The temporary public-read bucket policy was removed after validation.

## Remediation Boundary

The remediation Lambda intentionally enforces S3 Public Access Block.

It does not delete or modify the offending bucket policy.

This keeps the automated action deterministic and narrowly scoped while relying on S3 Block Public Access to prevent public access.

## Terraform Validation

Terraform reported:

`No changes`

The deployed infrastructure therefore matched the Terraform configuration during final validation.

## Unit Test Validation

Command:

`pytest -q tests/test_remediate_s3_public.py`

Result:

`3 passed in 0.56s`

## Validation Summary

The live security control was validated through the following path:

AWS Config

→ `NON_COMPLIANT`

→ Amazon EventBridge

→ AWS Lambda remediation

→ S3 Public Access Block enforced

→ AWS Config

→ `COMPLIANT`

Testing was performed only against the dedicated security-test bucket, and the temporary test policy was removed after validation.
