from cloudsec.risk import Finding


CONTROL_SEVERITY = {
    "cloud-security-autoremediation-s3-public-read-prohibited": "HIGH",
}


def normalize_config_event(event: dict) -> Finding:
    detail = event.get("detail", {})

    control = detail.get("configRuleName")
    resource_type = detail.get("resourceType")
    resource_id = detail.get("resourceId")

    if not control:
        raise ValueError("Missing Config rule name")

    if not resource_type:
        raise ValueError("Missing resource type")

    if not resource_id:
        raise ValueError("Missing resource ID")

    severity = CONTROL_SEVERITY.get(control, "MEDIUM")

    return Finding(
        control=control,
        resource_type=resource_type,
        resource_id=resource_id,
        severity=severity,
    )
