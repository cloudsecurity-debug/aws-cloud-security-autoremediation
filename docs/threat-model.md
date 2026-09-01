# Threat Model

## Objective

Detect and safely remediate common AWS cloud security misconfigurations before they create unnecessary exposure.

The design prioritizes narrow, deterministic remediation for security issues that can be safely corrected automatically.

## Assets

The primary protected asset in the current implementation is Amazon S3.

Security properties being protected include:

- Prevention of unintended public access
- Protection of stored data from accidental exposure
- Consistent security configuration
- Auditability of remediation activity

## Threat Scenarios

### S3 Public Exposure

An accidentally public S3 bucket can expose sensitive data to unauthorized users.

**Current control:**

AWS Config evaluates the S3 security posture. A `NON_COMPLIANT` result is designed to trigger EventBridge and the remediation Lambda, which enforces S3 Public Access Block.

### Insecure Network Access

A security group may permit unrestricted SSH access from the internet.

**Current status:**

Documented as a security scenario but not currently automated by this project.

### Missing Encryption

Data may be stored without the expected encryption controls.

**Current status:**

Documented as a security scenario but not currently automated by this project.

### Missing Audit Logging

CloudTrail or other audit controls may be unavailable or incorrectly configured, reducing visibility during an incident.

**Current status:**

Documented as a security scenario but not currently automated by this project.

## Trust Boundaries

The primary trust boundaries are:

1. AWS resource configuration
2. AWS Config compliance evaluation
3. EventBridge event routing
4. Lambda execution
5. IAM authorization
6. S3 security-control enforcement

Each boundary should be restricted to the minimum permissions and event scope required for the intended operation.

## Security Principle

The system must distinguish between:

- Safe automatic remediation
- Actions requiring human approval

Automatic remediation must be:

1. Deterministic
2. Reversible where possible
3. Scoped to the affected resource
4. Logged
5. Verified after execution
6. Non-destructive

## Current Automated Remediation

The current automated remediation is intentionally limited to S3 Public Access Block.

The Lambda enforces:

- `BlockPublicAcls`
- `IgnorePublicAcls`
- `BlockPublicPolicy`
- `RestrictPublicBuckets`

The remediation was directly tested against the controlled security-test bucket and the resulting S3 configuration was verified through the AWS API.

## Residual Risk

The project does not currently protect against every AWS security misconfiguration.

Examples include:

- Unrestricted network access
- Missing encryption on other resource types
- Missing CloudTrail controls
- Compromised IAM credentials
- Application-level vulnerabilities

These require additional detection and remediation controls or human investigation.

## Safe Testing

The project does not intentionally expose the test S3 bucket publicly merely to manufacture a security incident.

Testing uses controlled resources and synthetic events where appropriate.

This reduces the risk of creating a real security exposure while still validating the remediation behavior.
