"""
Verdict metadata mapping for deterministic summary and impact injection.

This module provides hardcoded summary and impact statements for each known verdict.
These are injected into the response AFTER the AI generates its diagnosis,
ensuring consistent, non-interpretive language for these fields.
"""

from typing import TypedDict


class VerdictInfo(TypedDict):
    summary: str
    impact: str


# Mapping of verdict strings to their deterministic summary and impact statements
VERDICT_METADATA: dict[str, VerdictInfo] = {
    "Context Hallucination": {
        "summary": "Agent claimed checks or facts that never actually occurred.",
        "impact": (
            "This creates confident-looking outputs that are silently wrong. "
            "In production, this can mislead decisions without triggering obvious errors. "
            "Users may trust fabricated information, leading to downstream failures."
        )
    },
    "Plan Collapse": {
        "summary": "Agent abandoned or failed to follow through on its stated plan.",
        "impact": (
            "The agent's reasoning became disconnected from its actions, leading to incomplete execution. "
            "This results in partial or inconsistent outputs that don't match the intended workflow. "
            "Critical steps may be skipped without any indication of failure."
        )
    },
    "Tool Misuse": {
        "summary": "Agent used tools incorrectly, with wrong parameters, or in inappropriate contexts.",
        "impact": (
            "Incorrect tool usage can produce invalid data, trigger errors, or waste resources. "
            "The agent may proceed with corrupted results, compounding the error through subsequent steps. "
            "This can lead to silent failures that are difficult to trace."
        )
    },
    "Unconstrained Autonomy": {
        "summary": "Agent took actions beyond its authorized scope or instructions.",
        "impact": (
            "Unrestricted agent behavior poses significant safety and control risks. "
            "The agent may modify systems, access data, or perform operations it shouldn't. "
            "This undermines trust and can cause unintended real-world consequences."
        )
    },
    "Goal Misalignment": {
        "summary": "Agent pursued objectives different from the user's actual intent.",
        "impact": (
            "The agent optimized for the wrong outcome, producing results that miss the point. "
            "Even technically correct outputs become useless if they don't serve the user's real goal. "
            "This wastes time and resources while failing to deliver value."
        )
    },
    "Premature Tool Usage": {
        "summary": "Agent invoked tools before adequately planning or understanding the task.",
        "impact": (
            "Acting before thinking leads to inefficient, scattered, or incorrect tool calls. "
            "The agent may miss important context or make irreversible actions prematurely. "
            "This often results in wasted API calls and suboptimal outcomes."
        )
    },
    "Missing Context": {
        "summary": "Agent lacked critical information needed to complete the task correctly.",
        "impact": (
            "Without essential context, the agent fills gaps with assumptions or defaults. "
            "Outputs may be technically valid but factually wrong or incomplete. "
            "Users receive plausible-looking results that fail on closer inspection."
        )
    },
    "Instruction Override": {
        "summary": "Agent ignored or contradicted explicit instructions from the user or system.",
        "impact": (
            "Disregarding instructions breaks the contract between user and agent. "
            "The agent becomes unpredictable, doing what it 'thinks' is right instead of what was asked. "
            "This erodes trust and makes the agent unreliable for critical tasks."
        )
    },
    "Looping Behavior": {
        "summary": "Agent got stuck in a repetitive cycle without making progress.",
        "impact": (
            "Infinite or excessive loops consume resources and time without advancing the task. "
            "The agent may repeatedly fail the same step or retry ineffective strategies. "
            "This can lead to timeouts, cost overruns, or system instability."
        )
    },
    "Error Propagation": {
        "summary": "Agent continued execution despite encountering errors, compounding the problem.",
        "impact": (
            "Ignoring errors allows failures to cascade through the workflow. "
            "Each subsequent step builds on corrupted or invalid data from the failed step. "
            "The final output may be completely wrong despite appearing successful."
        )
    },
}

# Default fallback for unknown verdicts
DEFAULT_VERDICT_INFO: VerdictInfo = {
    "summary": "Agent exhibited unexpected behavior that doesn't match known failure patterns.",
    "impact": (
        "The specific failure mode is not yet categorized in our diagnostic system. "
        "Manual review is recommended to understand the root cause and potential consequences. "
        "Consider adding this verdict type to improve future diagnostics."
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

