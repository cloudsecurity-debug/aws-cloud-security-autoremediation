import json
import os

import boto3

from cloudsec.engine import evaluate_event
from cloudsec.risk import RemediationDecision


lambda_client = boto3.client("lambda")


def lambda_handler(event, context):
    plan = evaluate_event(event)

    print(json.dumps({
        "decision": plan.decision.value,
        "action": plan.action,
    }))

    if plan.decision != RemediationDecision.AUTO_REMEDIATE:
        return {
            "statusCode": 200,
            "decision": plan.decision.value,
            "action": plan.action,
            "invoked": False,
        }

    bucket_name = event["detail"]["resourceId"]

    executor_name = os.environ["REMEDIATION_FUNCTION_NAME"]

    lambda_client.invoke(
        FunctionName=executor_name,
        InvocationType="RequestResponse",
        Payload=json.dumps({
            "bucket_name": bucket_name,
        }).encode(),
    )

    return {
        "statusCode": 200,
        "decision": plan.decision.value,
        "action": plan.action,
        "bucket": bucket_name,
        "invoked": True,
    }
