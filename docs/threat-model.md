# Threat Model

## Objective

Detect and safely remediate common AWS cloud security
misconfigurations before they create unnecessary exposure.

## Threat Scenarios

### S3 Public Exposure
An accidentally public S3 bucket exposes sensitive data.

### Insecure Network Access
A security group permits unrestricted SSH access from the internet.

### Missing Encryption
Data is stored without the expected encryption controls.

### Missing Audit Logging
CloudTrail is unavailable, reducing visibility during an incident.

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
