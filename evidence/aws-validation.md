# AWS Deployment Validation

## Project

AWS Cloud Security Auto-Remediation

## Region

`eu-north-1`

## Lambda Validation

Function: `cloud-security-autoremediation-remediation`

- State: `Active`
- Runtime: `Python 3.12`
- Last update status: `Successful`

## EventBridge Validation

Rule: `cloud-security-autoremediation-config-noncompliant`

- State: `ENABLED`
- Event source: `aws.config`
- Compliance type filter: `NON_COMPLIANT`
- Config rule: `cloud-security-autoremediation-s3-public-read-prohibited`

## EventBridge Target

One target was verified and points to the remediation Lambda.

The input transformer extracts `$.detail.resourceId`.

## Lambda Invocation Permissions

- `AllowAWSConfigInvoke`
- `AllowEventBridgeInvoke`

The EventBridge permission is scoped to the specific production rule.

## S3 Remediation Validation

The remediation Lambda was directly tested against the controlled security-test bucket.

- HTTP status: `200`
- Action: `public_access_block_enforced`

All four S3 Public Access Block controls were confirmed enabled:

- `BlockPublicAcls: true`
- `IgnorePublicAcls: true`
- `BlockPublicPolicy: true`
- `RestrictPublicBuckets: true`

## Terraform Validation

Terraform previously reported `No changes`.

## Unit Test Validation

Command: `pytest -q tests/test_remediate_s3_public.py`

Result: `3 passed in 0.56s`

## Validation Boundary

A complete live AWS-generated `NON_COMPLIANT` event flowing through AWS Config → EventBridge → Lambda has not been intentionally manufactured.

Testing used controlled resources and synthetic events where appropriate. No public S3 exposure was intentionally created merely to generate a security incident.
