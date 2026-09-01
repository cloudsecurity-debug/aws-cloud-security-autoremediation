from cloudsec.remediation import build_remediation_plan
from cloudsec.risk import Finding, RemediationDecision


def test_s3_public_read_creates_auto_remediation_plan():
    finding = Finding(
        control="S3_PUBLIC_READ_PROHIBITED",
        resource_type="AWS::S3::Bucket",
        resource_id="test-bucket",
        severity="HIGH",
    )

    plan = build_remediation_plan(finding)

    assert plan.decision == RemediationDecision.AUTO_REMEDIATE
    assert plan.action == "ENFORCE_S3_PUBLIC_ACCESS_BLOCK"


def test_high_risk_finding_requires_review():
    finding = Finding(
        control="IAM_EXCESSIVE_PERMISSIONS",
        resource_type="AWS::IAM::Role",
        resource_id="test-role",
        severity="HIGH",
    )

    plan = build_remediation_plan(finding)

    assert plan.decision == RemediationDecision.HUMAN_APPROVAL
    assert plan.action == "REVIEW_FINDING"


def test_low_risk_finding_is_report_only():
    finding = Finding(
        control="EXAMPLE_LOW_RISK",
        resource_type="AWS::Example::Resource",
        resource_id="example",
        severity="LOW",
    )

    plan = build_remediation_plan(finding)

    assert plan.decision == RemediationDecision.REPORT_ONLY
    assert plan.action == "REPORT_FINDING"
