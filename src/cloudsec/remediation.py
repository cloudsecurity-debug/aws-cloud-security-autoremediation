from dataclasses import dataclass

from cloudsec.risk import Finding, RemediationDecision, classify_finding


@dataclass(frozen=True)
class RemediationPlan:
    decision: RemediationDecision
    action: str


def build_remediation_plan(finding: Finding) -> RemediationPlan:
    decision = classify_finding(finding)

    if decision == RemediationDecision.AUTO_REMEDIATE:
        return RemediationPlan(
            decision=decision,
            action="ENFORCE_S3_PUBLIC_ACCESS_BLOCK",
        )

    if decision == RemediationDecision.HUMAN_APPROVAL:
        return RemediationPlan(
            decision=decision,
            action="REVIEW_FINDING",
        )

    return RemediationPlan(
        decision=decision,
        action="REPORT_FINDING",
    )
