import pytest

from cloudsec.events import normalize_config_event
from cloudsec.risk import Finding


def test_normalize_s3_config_event():
    event = {
        "detail": {
            "configRuleName": (
                "cloud-security-autoremediation-"
                "s3-public-read-prohibited"
            ),
            "resourceType": "AWS::S3::Bucket",
            "resourceId": "security-test-bucket",
        }
    }

    finding = normalize_config_event(event)

    assert finding == Finding(
        control="S3_PUBLIC_READ_PROHIBITED",
        resource_type="AWS::S3::Bucket",
        resource_id="security-test-bucket",
        severity="HIGH",
    )


def test_unknown_control_gets_medium_severity():
    event = {
        "detail": {
            "configRuleName": "UNKNOWN_CONTROL",
            "resourceType": "AWS::IAM::Role",
            "resourceId": "test-role",
        }
    }

    finding = normalize_config_event(event)

    assert finding.control == "UNKNOWN_CONTROL"
    assert finding.severity == "MEDIUM"


@pytest.mark.parametrize(
    "missing_field",
    ["configRuleName", "resourceType", "resourceId"],
)
def test_missing_required_field_is_rejected(missing_field):
    event = {
        "detail": {
            "configRuleName": "example-control",
            "resourceType": "AWS::S3::Bucket",
            "resourceId": "bucket",
        }
    }

    del event["detail"][missing_field]

    with pytest.raises(ValueError):
        normalize_config_event(event)
