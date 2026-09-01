from cloudsec.events import normalize_config_event
from cloudsec.remediation import build_remediation_plan
from cloudsec.risk import RemediationDecision


def test_config_event_produces_s3_auto_remediation_plan():
    event = {
        "source": "aws.config",
        "detail-type": "Config Rules Compliance Change",
        "detail": {
            "configRuleName": (
                "cloud-security-autoremediation-"
                "s3-public-read-prohibited"
            ),
            "resourceType": "AWS::S3::Bucket",
            "resourceId": "security-test-bucket",
            "newEvaluationResult": {
                "complianceType": "NON_COMPLIANT",
            },
        },
    }

    finding = normalize_config_event(event)
    plan = build_remediation_plan(finding)

    assert plan.decision == RemediationDecision.AUTO_REMEDIATE
    assert plan.action == "ENFORCE_S3_PUBLIC_ACCESS_BLOCK"
