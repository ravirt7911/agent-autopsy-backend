"""
Pydantic models for request and response schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class DiagnosisRequest(BaseModel):
    agent_goal: str = Field(..., description="What the agent was supposed to accomplish")
    instructions: str = Field(..., description="The instructions or system prompt given to the agent")
    execution_steps: str = Field(..., description="The steps the agent took, including tool calls and reasoning")
    final_output: str = Field(..., description="The final output produced by the agent")
    expected_output: Optional[str] = Field(None, description="Optional: What the output should have been")

    model_config = {
        "json_schema_extra": {
            "example": {
                "agent_goal": "Find and summarize recent AI safety papers",
                "instructions": "You are a research assistant. Always plan before taking action.",
                "execution_steps": "Step 1: Called search_papers() immediately without planning\nStep 2: Got 100 results\nStep 3: Summarized first 3 papers",
                "final_output": "Here are 3 papers about AI safety...",
                "expected_output": "A comprehensive summary of the 10 most recent and relevant papers"
            }
        }
    }


class FailurePoint(BaseModel):
    step_number: int = Field(..., description="The step number where the agent first failed or went wrong")
    step_description: str = Field(..., description="Brief description of what happened at that step")
    reason: str = Field(..., description="Why this step caused the failure")


class DiagnosisResponse(BaseModel):
    verdict: str = Field(..., description="The primary failure type identified")
    explanation: str = Field(..., description="Plain English explanation of what went wrong")
    evidence: List[str] = Field(..., description="Specific examples from the execution that support the verdict")
    recommended_fix: str = Field(..., description="One clear, actionable recommendation")
    confidence: str = Field(..., description="Confidence level: high, medium, or low")
    failure_point: FailurePoint = Field(..., description="The specific step where the failure occurred")

