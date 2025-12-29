"""
Core diagnostic engine that analyzes agent failures using LLM
"""
import json
import asyncio
from openai import AsyncOpenAI
from app.models.schemas import DiagnosisRequest, DiagnosisResponse, FailurePoint
from app.prompts import DIAGNOSTIC_SYSTEM_PROMPT, build_diagnostic_prompt
from app.config import settings
from app.verdict_metadata import get_verdict_metadata

# Initialize OpenAI client lazily
_client = None


def get_client() -> AsyncOpenAI:
    """Get or create the OpenAI client instance"""
    global _client
    if _client is None:
        settings.validate()
        _client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    return _client


async def diagnose_agent_failure(request: DiagnosisRequest) -> DiagnosisResponse:
    """
    Main diagnostic function that analyzes an agent failure using GPT-4
    
    Args:
        request: DiagnosisRequest containing agent execution details
        
    Returns:
        DiagnosisResponse with verdict, explanation, evidence, and fix
        
    Raises:
        Exception: If LLM call fails after retries or returns invalid data
    """
    
    for attempt in range(settings.MAX_RETRIES):
        try:
            # Build the diagnostic prompt
            user_prompt = build_diagnostic_prompt(request)
            
            # Call OpenAI API
            client = get_client()
            response = await client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": DIAGNOSTIC_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=settings.OPENAI_TEMPERATURE,
                response_format={"type": "json_object"},  # Ensure JSON response
            )
            
            # Extract and parse the response
            result_text = response.choices[0].message.content
            result_json = json.loads(result_text)
            
            # Validate required fields
            required_fields = ["verdict", "explanation", "evidence", "recommended_fix", "failure_point"]
            for field in required_fields:
                if field not in result_json:
                    raise ValueError(f"Missing required field: {field}")
            
            # Ensure evidence is a list
            if not isinstance(result_json["evidence"], list):
                result_json["evidence"] = [result_json["evidence"]]
            
            # Set default confidence if missing
            if "confidence" not in result_json:
                result_json["confidence"] = "medium"
            
            # Validate failure_point structure
            fp = result_json["failure_point"]
            if not isinstance(fp, dict):
                raise ValueError("failure_point must be an object")
            for fp_field in ["step_number", "step_description", "reason"]:
                if fp_field not in fp:
                    raise ValueError(f"failure_point missing required field: {fp_field}")
            
            # Create FailurePoint object
            failure_point = FailurePoint(
                step_number=fp["step_number"],
                step_description=fp["step_description"],
                reason=fp["reason"]
            )
            
            # Inject deterministic verdict metadata (not AI-generated)
            verdict_metadata = get_verdict_metadata(result_json["verdict"])
            
            # Return validated response with injected metadata
            return DiagnosisResponse(
                verdict=result_json["verdict"],
                verdict_summary=verdict_metadata["summary"],
                impact_statement=verdict_metadata["impact"],
                explanation=result_json["explanation"],
                evidence=result_json["evidence"],
                recommended_fix=result_json["recommended_fix"],
                confidence=result_json["confidence"],
                failure_point=failure_point
            )
            
        except json.JSONDecodeError as e:
            if attempt == settings.MAX_RETRIES - 1:
                raise Exception(f"LLM returned invalid JSON after {settings.MAX_RETRIES} attempts: {str(e)}")
            print(f"JSON decode error on attempt {attempt + 1}, retrying...")
            await asyncio.sleep(settings.RETRY_DELAY)
            
        except ValueError as e:
            if attempt == settings.MAX_RETRIES - 1:
                raise Exception(f"LLM response missing required fields: {str(e)}")
            print(f"Validation error on attempt {attempt + 1}, retrying...")
            await asyncio.sleep(settings.RETRY_DELAY)
            
        except Exception as e:
            if attempt == settings.MAX_RETRIES - 1:
                raise Exception(f"Diagnosis failed after {settings.MAX_RETRIES} attempts: {str(e)}")
            print(f"Error on attempt {attempt + 1}: {str(e)}, retrying...")
            await asyncio.sleep(settings.RETRY_DELAY)
    
    # Should never reach here due to the raise in the final attempt
    raise Exception("Unexpected error in diagnosis")

