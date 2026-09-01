import importlib.util
import os

from cloudsec.risk import RemediationDecision


def load_decision_module():
    path = "terraform/lambda/decision/decision.py"
    spec = importlib.util.spec_from_file_location("decision", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_auto_remediation_invokes_executor(monkeypatch):
    module = load_decision_module()

    os.environ["REMEDIATION_FUNCTION_NAME"] = "test-remediation"

    calls = []

    def fake_invoke(**kwargs):
        calls.append(kwargs)
        return {"StatusCode": 200}

    monkeypatch.setattr(module.lambda_client, "invoke", fake_invoke)

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

    result = module.lambda_handler(event, None)

    assert result["decision"] == RemediationDecision.AUTO_REMEDIATE.value
    assert result["action"] == "ENFORCE_S3_PUBLIC_ACCESS_BLOCK"
    assert result["invoked"] is True

    assert calls[0]["FunctionName"] == "test-remediation"
    assert calls[0]["InvocationType"] == "RequestResponse"
