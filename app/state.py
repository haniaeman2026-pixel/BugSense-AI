from typing import TypedDict, List

class BugState(TypedDict, total=False):
    bug_description: str
    bug_title: str
    affected_feature: str
    issue_summary: str
    severity: str
    severity_reason: str
    possible_root_causes: List[str]
    formatted_report: dict
    error: str
