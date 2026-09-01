# Architecture

## Overview

This project implements an AWS cloud security detection and automated remediation pipeline using Terraform, AWS Config, Amazon EventBridge, AWS Lambda, Python, IAM, Amazon S3, and CloudWatch.

The primary use case is detecting S3 public-access misconfiguration and automatically enforcing S3 Public Access Block controls.

## Architecture Flow

```text
Amazon S3
    |
    v
AWS Config
    |
    | NON_COMPLIANT
    v
Amazon EventBridge
    |
    v
AWS Lambda
    |
    v
S3 Public Access Block
```




## Components

### Amazon S3

The project provisions a dedicated AWS Config bucket and a security test bucket with security controls including Public Access Block and server-side encryption.

### AWS Config

AWS Config records resource configuration and evaluates S3 resources against:

`cloud-security-autoremediation-s3-public-read-prohibited`

The rule identifies S3 resources that violate the required public-access security posture.

### Amazon EventBridge

EventBridge listens for AWS Config compliance-change events.

The production rule targets `NON_COMPLIANT` results from the S3 public-read Config rule.

### AWS Lambda

The remediation function runs on Python 3.12:

`cloud-security-autoremediation-remediation`

Its responsibility is intentionally narrow: enforce the required S3 Public Access Block configuration.

### IAM

The Lambda uses a dedicated execution role with permissions required for the remediation operation.

### CloudWatch Logs

Lambda execution logs provide visibility into remediation invocations and execution results.

## Security Design

The architecture follows:

- Least privilege
- Event-driven detection
- Narrowly scoped remediation
- Infrastructure as Code
- Observable execution

## Validation

The deployed infrastructure was validated with Terraform and AWS service-level checks.

Verified components include:

- Terraform state consistency
- Active AWS Config recorder
- Active AWS Config rule
- Enabled EventBridge rule
- Active Lambda function
- Successful Lambda update
- Successful Lambda remediation test
- AWS Config Lambda permission
- EventBridge Lambda permission
- Exactly one EventBridge target
- CloudWatch Lambda execution logs
- S3 Public Access Block enforcement
- All four S3 Public Access Block controls confirmed enabled
- Lambda unit tests passing

The remediation Lambda was directly tested against the controlled security-test bucket. The function returned a successful response and the resulting S3 Public Access Block configuration was verified through the AWS API.

The EventBridge rule, target, and permissions were independently verified. A controlled live test was performed against the dedicated security-test bucket, producing an AWS Config `NON_COMPLIANT` evaluation and subsequent `COMPLIANT` evaluation after remediation.

The temporary public-read policy was removed after validation. No unrelated or production S3 resources were intentionally exposed.

## Current Boundary

The current implementation focuses on S3 public-access protection.

Other scenarios such as unrestricted SSH access, missing encryption on arbitrary resources, and missing CloudTrail logging are documented as security concerns but are not currently automated by this remediation pipeline.
