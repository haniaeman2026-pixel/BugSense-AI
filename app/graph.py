import json
import re
from typing import Any
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from app.state import BugState
from app.prompts import (
    BUG_ANALYSIS_PROMPT, SEVERITY_PROMPT,
    ROOT_CAUSE_PROMPT, REPORT_PROMPT
)

def _json_from_text(content: Any) -> dict:
    if isinstance(content, list):
        content = "".join(str(part.get("text", "")) if isinstance(part, dict) else str(part) for part in content)
    text = str(content).strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.S)
        if match:
            return json.loads(match.group(0))
        raise ValueError("The AI returned a response that was not valid JSON.")

def _model():
    # Set GROQ_MODEL in .env to change the model if needed.
    import os
    return ChatGroq(
        model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        temperature=0.2,
        timeout=60,
        max_retries=2,
    )

def bug_analysis_node(state: BugState) -> dict:
    response = _model().invoke(BUG_ANALYSIS_PROMPT.format(bug_description=state["bug_description"]))
    data = _json_from_text(response.content)
    return {
        "bug_title": str(data.get("bug_title", "Software issue reported"))[:180],
        "affected_feature": str(data.get("affected_feature", "Not specified"))[:180],
        "issue_summary": str(data.get("issue_summary", "Not enough information provided."))[:1200],
    }

def severity_detection_node(state: BugState) -> dict:
    analysis = {
        "bug_title": state.get("bug_title", ""),
        "affected_feature": state.get("affected_feature", ""),
        "issue_summary": state.get("issue_summary", ""),
    }
    response = _model().invoke(SEVERITY_PROMPT.format(
        bug_description=state["bug_description"],
        analysis=json.dumps(analysis, ensure_ascii=False)
    ))
    data = _json_from_text(response.content)
    severity = str(data.get("severity", "Medium")).title()
    if severity not in {"Critical", "High", "Medium", "Low"}:
        severity = "Medium"
    return {
        "severity": severity,
        "severity_reason": str(data.get("severity_reason", "Impact requires further investigation."))[:1000]
    }

def root_cause_node(state: BugState) -> dict:
    analysis = {
        "bug_title": state.get("bug_title", ""),
        "affected_feature": state.get("affected_feature", ""),
        "issue_summary": state.get("issue_summary", ""),
        "severity": state.get("severity", "Medium"),
    }
    response = _model().invoke(ROOT_CAUSE_PROMPT.format(
        bug_description=state["bug_description"],
        analysis=json.dumps(analysis, ensure_ascii=False)
    ))
    data = _json_from_text(response.content)
    causes = data.get("possible_root_causes", [])
    if not isinstance(causes, list):
        causes = [str(causes)]
    causes = [str(c).strip() for c in causes if str(c).strip()][:5]
    if not causes:
        causes = ["Insufficient information to suggest a specific cause; inspect logs and reproduce the issue."]
    return {"possible_root_causes": causes}

def format_report_node(state: BugState) -> dict:
    data = {
        "title": state.get("bug_title", "Software issue reported"),
        "affected_feature": state.get("affected_feature", "Not specified"),
        "summary": state.get("issue_summary", ""),
        "severity": state.get("severity", "Medium"),
        "severity_reason": state.get("severity_reason", ""),
        "possible_root_causes": state.get("possible_root_causes", []),
        "original_description": state["bug_description"],
    }
    response = _model().invoke(REPORT_PROMPT.format(data=json.dumps(data, ensure_ascii=False)))
    report = _json_from_text(response.content)
    # Keep the required fields reliable even if the model omits a key.
    report.setdefault("title", data["title"])
    report.setdefault("affected_feature", data["affected_feature"])
    report.setdefault("summary", data["summary"])
    report.setdefault("severity", data["severity"])
    report.setdefault("severity_reason", data["severity_reason"])
    report.setdefault("possible_root_causes", data["possible_root_causes"])
    report.setdefault("original_description", data["original_description"])
    report.setdefault("investigation_notes", "Root causes are hypotheses. Verify them using reproduction steps, logs, and code.")
    return {"formatted_report": report}

def build_graph():
    workflow = StateGraph(BugState)
    workflow.add_node("bug_analysis", bug_analysis_node)
    workflow.add_node("severity_detection", severity_detection_node)
    workflow.add_node("root_cause_suggestion", root_cause_node)
    workflow.add_node("format_report", format_report_node)
    workflow.add_edge(START, "bug_analysis")
    workflow.add_edge("bug_analysis", "severity_detection")
    workflow.add_edge("severity_detection", "root_cause_suggestion")
    workflow.add_edge("root_cause_suggestion", "format_report")
    workflow.add_edge("format_report", END)
    return workflow.compile()
