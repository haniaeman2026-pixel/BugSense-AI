BUG_ANALYSIS_PROMPT = """You are a careful software QA analyst.
Analyze the user's bug description. Return ONLY valid JSON with these keys:
bug_title (short, clear title), affected_feature (feature/component), issue_summary
(1-3 concise sentences describing observed behavior and expected behavior if inferable).
Do not invent facts. If information is missing, say it is not specified.
Bug description:
{bug_description}
"""

SEVERITY_PROMPT = """You are a software QA triage specialist.
Classify the bug as exactly one of: Critical, High, Medium, Low.
Consider impact, scope, availability of workarounds, and data/security risk.
Return ONLY valid JSON with keys severity and severity_reason.
Do not exaggerate impact; if details are insufficient, use a cautious classification and
explain what additional impact information is needed.
Bug description: {bug_description}
Analysis: {analysis}
"""

ROOT_CAUSE_PROMPT = """You are an experienced software debugging assistant.
Suggest 3-5 plausible root causes based only on the supplied description and analysis.
These are hypotheses, not confirmed findings. Return ONLY valid JSON:
{{"possible_root_causes": ["...", "...", "..."]}}
Prefer actionable technical possibilities. Do not claim to have inspected code or logs.
Bug description: {bug_description}
Analysis: {analysis}
"""

REPORT_PROMPT = """Create a clean structured software bug report using only the provided data.
Return ONLY valid JSON with keys:
title, affected_feature, summary, severity, severity_reason,
possible_root_causes (array), original_description, investigation_notes.
investigation_notes should remind the reader that root causes are hypotheses and should be
verified with logs, reproduction steps, and code. Do not add unsupported facts.
Input data:
{data}
"""
