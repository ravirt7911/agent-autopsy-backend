"""
Verdict metadata mapping for deterministic summary and impact injection.

This module provides hardcoded summary and impact statements for each known verdict.
These are injected into the response AFTER the AI generates its diagnosis,
ensuring consistent, non-interpretive language for these fields.

Design principles:
- Summaries should be opinionated and specific, highlighting what the agent optimized for incorrectly
- Impact statements should include concrete business consequences for real teams (PMs, engineers, etc.)
- Avoid generic phrasing like "reduces value" or "pursued different objectives"
"""

from typing import TypedDict


class VerdictInfo(TypedDict):
    summary: str
    impact: str


# Mapping of verdict strings to their deterministic summary and impact statements
VERDICT_METADATA: dict[str, VerdictInfo] = {
    "Context Hallucination": {
        "summary": "Agent fabricated verification steps or invented facts it never actually checked.",
        "impact": (
            "Engineers waste hours debugging issues that don't exist because they trust the agent's false claims. "
            "Teams may ship 'fixes' for fabricated bugs, introducing real problems while ignoring actual failures. "
            "In code review or QA workflows, fabricated test results can let broken code reach production."
        )
    },
    "Plan Collapse": {
        "summary": "Agent generated a coherent plan then ignored it, executing disconnected actions instead.",
        "impact": (
            "Engineers receive half-implemented features that look complete but miss critical steps. "
            "QA teams waste cycles testing incomplete functionality that was supposed to be finished. "
            "Sprint commitments slip because work marked 'done' requires unexpected follow-up to actually complete."
        )
    },
    "Tool Misuse": {
        "summary": "Agent called tools with malformed inputs or in contexts where they couldn't succeed.",
        "impact": (
            "Malformed API requests trigger rate limits or account flags, blocking legitimate operations. "
            "Databases may ingest corrupted records that break downstream queries and reports. "
            "Engineers spend debugging time tracing failures back to obviously wrong tool parameters."
        )
    },
    "Unconstrained Autonomy": {
        "summary": "Agent exceeded its authorized scope, performing operations it wasn't permitted to do.",
        "impact": (
            "Unauthorized data access creates compliance violations that require incident reports and audits. "
            "Unreviewed code or config changes pushed by the agent can break production systems. "
            "Security teams lose trust in agent systems, leading to restrictive policies that slow all automation."
        )
    },
    "Goal Misalignment": {
        "summary": "Agent optimized for surface-level patterns instead of the stated business objective.",
        "impact": (
            "Teams prioritize the wrong problems during product planning because analysis highlighted noise over signal. "
            "Engineering effort gets wasted building features that address symptoms instead of root causes. "
            "PMs present misleading metrics to stakeholders, leading to strategic decisions based on irrelevant data."
        )
    },
    "Premature Tool Usage": {
        "summary": "Agent jumped to tool execution before understanding requirements, wasting calls on wrong queries.",
        "impact": (
            "API costs spike from unnecessary calls that retrieve irrelevant data or fail outright. "
            "Rate limits get exhausted early, blocking the agent from making calls when they'd actually help. "
            "Engineers inherit search results or data pulls that don't match what was actually needed."
        )
    },
    "Missing Context": {
        "summary": "Agent filled knowledge gaps with assumptions instead of asking for clarification.",
        "impact": (
            "Reports and analyses are generated using wrong baseline assumptions that invalidate conclusions. "
            "Decisions get made on incomplete data analysis that looks comprehensive but misses key constraints. "
            "Engineers build against assumed requirements, then rework when actual specs finally surface."
        )
    },
    "Instruction Override": {
        "summary": "Agent substituted its own judgment for explicit instructions, doing what it deemed 'better'.",
        "impact": (
            "Automation pipelines fail in production because the agent 'improved' on working instructions. "
            "Teams can't rely on agent behavior being consistent, forcing manual review of all outputs. "
            "Engineering time shifts from building features to babysitting unpredictable agent behavior."
        )
    },
    "Looping Behavior": {
        "summary": "Agent repeated the same failing operation, burning through resources without progress.",
        "impact": (
            "Inference budgets get exhausted on a single stuck task, blocking other work that needs the same quota. "
            "Request timeouts delay user-facing workflows that depend on agent completion. "
            "Engineers get paged for runaway processes that should have failed fast and escalated."
        )
    },
    "Error Propagation": {
        "summary": "Agent treated errors as soft warnings, pushing forward with corrupted state instead of stopping.",
        "impact": (
            "Bad data flows into dashboards and reports, causing teams to make decisions on invalid metrics. "
            "Downstream systems ingest corrupted outputs that trigger cascading failures hours later. "
            "Engineers face multi-step debugging to trace production issues back to an ignored early error."
        )
    },
}

# Default fallback for unknown verdicts
DEFAULT_VERDICT_INFO: VerdictInfo = {
    "summary": "Agent exhibited a failure pattern not yet categorized in the diagnostic system.",
    "impact": (
        "This failure mode requires manual review to assess business impact and root cause. "
        "Engineering time will be needed to investigate before this agent can be trusted for similar tasks. "
        "Consider filing an issue to add this verdict type for better automated diagnosis in the future."
    )
}


def get_verdict_metadata(verdict: str) -> VerdictInfo:
    """
    Retrieve the summary and impact for a given verdict.
    
    Args:
        verdict: The verdict string returned by the AI diagnosis
        
    Returns:
        VerdictInfo containing summary and impact strings.
        Falls back to DEFAULT_VERDICT_INFO if verdict is unknown.
    """
    return VERDICT_METADATA.get(verdict, DEFAULT_VERDICT_INFO)

