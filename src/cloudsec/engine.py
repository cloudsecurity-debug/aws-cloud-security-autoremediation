from cloudsec.events import normalize_config_event
from cloudsec.remediation import build_remediation_plan


def evaluate_event(event: dict):
    finding = normalize_config_event(event)
    return build_remediation_plan(finding)
