from cloudsec.risk import (
    Finding,
    RemediationDecision,
    classify_finding,
)


def test_s3_public_read_is_auto_remediable():
    finding = Finding(
        control="S3_PUBLIC_READ_PROHIBITED",
        resource_type="AWS::S3::Bucket",
        resource_id="test-bucket",
        severity="HIGH",
    )

    assert classify_finding(finding) == RemediationDecision.AUTO_REMEDIATE


def test_high_risk_unknown_control_requires_human_approval():
    finding = Finding(
        control="IAM_EXCESSIVE_PERMISSIONS",
        resource_type="AWS::IAM::Role",
        resource_id="test-role",
        severity="HIGH",
    )

    assert classify_finding(finding) == RemediationDecision.HUMAN_APPROVAL


def test_low_risk_unknown_control_is_report_only():
    finding = Finding(
        control="EXAMPLE_LOW_RISK",
        resource_type="AWS::Example::Resource",
        resource_id="example-resource",
        severity="LOW",
    )

    assert classify_finding(finding) == RemediationDecision.REPORT_ONLY


def test_s3_control_with_wrong_resource_type_is_not_auto_remediated():
    finding = Finding(
        control="S3_PUBLIC_READ_PROHIBITED",
        resource_type="AWS::IAM::Role",
        resource_id="unexpected-resource",
        severity="HIGH",
    )

    assert classify_finding(finding) == RemediationDecision.HUMAN_APPROVAL
