from cloudsec.risk import Finding


CONTROL_MAP = {
    "cloud-security-autoremediation-s3-public-read-prohibited": (
        "S3_PUBLIC_READ_PROHIBITED",
        "HIGH",
    ),
}


def normalize_config_event(event: dict) -> Finding:
    detail = event.get("detail", {})

    config_rule_name = detail.get("configRuleName")
    resource_type = detail.get("resourceType")
    resource_id = detail.get("resourceId")

    if not config_rule_name:
        raise ValueError("Missing Config rule name")

    if not resource_type:
        raise ValueError("Missing resource type")

    if not resource_id:
        raise ValueError("Missing resource ID")

    control, severity = CONTROL_MAP.get(
        config_rule_name,
        (config_rule_name, "MEDIUM"),
    )

    return Finding(
        control=control,
        resource_type=resource_type,
        resource_id=resource_id,
        severity=severity,
    )
