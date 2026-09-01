from cloudsec.engine import evaluate_event
from cloudsec.risk import RemediationDecision


def test_engine_evaluates_s3_config_event():
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

    plan = evaluate_event(event)

    assert plan.decision == RemediationDecision.AUTO_REMEDIATE
    assert plan.action == "ENFORCE_S3_PUBLIC_ACCESS_BLOCK"
