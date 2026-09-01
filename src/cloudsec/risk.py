from dataclasses import dataclass
from enum import Enum


class RemediationDecision(str, Enum):
    AUTO_REMEDIATE = "AUTO_REMEDIATE"
    HUMAN_APPROVAL = "HUMAN_APPROVAL"
    REPORT_ONLY = "REPORT_ONLY"


@dataclass(frozen=True)
class Finding:
    control: str
    resource_type: str
    resource_id: str
    severity: str


AUTO_REMEDIABLE_CONTROLS = {
    ("S3_PUBLIC_READ_PROHIBITED", "AWS::S3::Bucket"),
}


def classify_finding(finding: Finding) -> RemediationDecision:
    control_key = (finding.control, finding.resource_type)

    if control_key in AUTO_REMEDIABLE_CONTROLS:
        return RemediationDecision.AUTO_REMEDIATE

    if finding.severity.upper() in {"CRITICAL", "HIGH"}:
        return RemediationDecision.HUMAN_APPROVAL

    return RemediationDecision.REPORT_ONLY
