# AWS Cloud Security Auto-Remediation

A Terraform-managed AWS security automation project that detects S3 public-access misconfigurations and safely enforces remediation using AWS Config, Amazon EventBridge, AWS Lambda, Python, IAM, and Amazon S3.

## Project Overview

Cloud security failures are often caused by configuration drift or accidental changes rather than sophisticated attacks.

This project demonstrates an event-driven security control that:

1. Monitors AWS resource configuration with AWS Config.
2. Detects an S3 public-access compliance violation.
3. Routes the compliance event through Amazon EventBridge.
4. Invokes a dedicated AWS Lambda remediation function.
5. Enforces S3 Public Access Block on the affected bucket.
6. Records Lambda execution activity in CloudWatch Logs.

## Architecture



## Security Controls

- S3 Public Access Block
- S3 server-side encryption
- S3 versioning
- AWS Config compliance monitoring
- EventBridge event filtering
- Dedicated Lambda execution role
- Least-privilege IAM permissions
- CloudWatch Lambda logging
- Terraform Infrastructure as Code

## AWS Services

| Service | Purpose |
|---|---|
| Amazon S3 | Protected resources and AWS Config delivery |
| AWS Config | Configuration recording and compliance evaluation |
| Amazon EventBridge | Event-driven remediation trigger |
| AWS Lambda | Automated security remediation |
| AWS IAM | Least-privilege authorization |
| Amazon CloudWatch Logs | Lambda execution visibility |
| Terraform | Infrastructure as Code |

## Automated Remediation

The current automated control focuses on S3 public-access protection.

The remediation Lambda runs on Python 3.12 and applies the required S3 Public Access Block configuration.

The Lambda operates through a dedicated IAM execution role rather than long-lived AWS access keys.

## Validation

Verified:

- Terraform reports no infrastructure changes.
- AWS Config recorder is active and reporting SUCCESS.
- AWS Config recording is enabled.
- The S3 public-read Config rule is ACTIVE.
- EventBridge production rule is enabled.
- Lambda remediation was successfully invoked.
- EventBridge-to-Lambda integration was successfully tested with a controlled synthetic event.
- Lambda execution was observed in CloudWatch Logs.
- Temporary test resources were removed after testing.

The project intentionally did not make the S3 bucket publicly accessible merely to manufacture a live security incident.

## Threat Model

The project considers:

- Accidental S3 public exposure
- Insecure network access
- Missing encryption
- Missing audit logging

Only the S3 public-access scenario is currently automated.

See  and .

## Design Principles

### Least Privilege

The remediation Lambda uses a dedicated IAM role with only the permissions required for its security operation.

### Deterministic Remediation

The remediation applies a known secure S3 configuration rather than making broad or unpredictable changes.

### Scoped Automation

The automated action is deliberately limited to S3 Public Access Block.

### Infrastructure as Code

Terraform defines the AWS infrastructure so the configuration can be reviewed, reproduced, and version controlled.

### Safe Testing

Integration testing used a controlled synthetic EventBridge event. The S3 bucket was not intentionally exposed to create a security failure.

## Known Limitations

The project has not demonstrated a complete live AWS-generated NON_COMPLIANT failure event from AWS Config through EventBridge into Lambda.

The EventBridge-to-Lambda integration was independently validated, while AWS Config was verified to be active and evaluating the resources.

This distinction is documented intentionally rather than claiming an unperformed test.

## Future Improvements

- Add CloudWatch alarms for remediation failures.
- Add automated unit tests.
- Add structured security-event logging.
- Add additional low-risk AWS Config rules.
- Add approval workflows for high-impact remediation.
- Integrate Prowler into CI/CD security checks.
- Add automated evidence collection.
- Add retry and dead-letter handling for failed remediation events.

## Portfolio Value

This project demonstrates practical experience with AWS cloud security, security automation, Infrastructure as Code, IAM least privilege, configuration compliance, event-driven architecture, serverless remediation, security testing, threat modeling, and operational logging.

## Repository Structure
