from collections import Counter
from langchain_core.documents import Document
from typing import Any, Dict, List
import json
import re
from utils.logger import logger
from utils.prompt_templates import TRAVEL_PLAN_GENERATION_PROMPT
from models.travel_models import *
from utils.config import settings
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

_cached_llm = None
_cached_plan_chain = None

def _get_llm():
    global _cached_llm
    if _cached_llm is None:
        _cached_llm = ChatOpenAI(
            temperature=settings.OPENAI_TEMPERATURE,
            model_name=settings.OPENAI_DEFAULT_MODEL,
            max_tokens=settings.OPENAI_MAX_TOKENS,
        )
    return _cached_llm


def _get_travel_plan_generation_chain():
    global _cached_plan_chain
    if _cached_plan_chain is None:
        llm = _get_llm()
        prompt = PromptTemplate.from_template(TRAVEL_PLAN_GENERATION_PROMPT)
        _cached_plan_chain = prompt | llm
    return _cached_plan_chain

def _get_request_data(travel_request: TravelRequest) -> Dict[str,Any]:
  result = dict[str,Any]()

  result["location"] = travel_request.location
  result["number_of_days"] = travel_request.number_of_days
  result["start_date"] = travel_request.start_date.strftime('%Y-%m-%d')
  result["preferred_language"] = travel_request.preferred_language
  result["interests_str"] = ", ".join(travel_request.interests) if travel_request.interests else "general tourism"
  result["budget_level"] = travel_request.budget_level

  return result


def _extract_json_from_response(response_text: str) -> str:
    if not response_text or not response_text.strip():
        raise ValueError("Empty response from LLM")

    # First try to extract JSON from markdown code blocks
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", response_text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Then try to find JSON object boundaries
    match = re.search(r"\{.*\}", response_text, re.DOTALL)
    if match:
        return match.group(0).strip()

    return response_text.strip()


def _fix_common_json_issues(json_str: str, error_pos: int = None) -> str:
    """Attempt to fix common JSON syntax errors from LLM responses"""
    fixed = json_str
    
    # Fix trailing commas before closing braces/brackets (safe fix)
    fixed = re.sub(r',(\s*[}\]])', r'\1', fixed)
    
    # If we know the error position, try to fix around that area first
    if error_pos is not None:
        # Look for missing comma before the error position
        start = max(0, error_pos - 150)
        end = min(len(fixed), error_pos + 150)
        before_error = fixed[:start]
        error_region = fixed[start:end]
        after_error = fixed[end:]
        
        # Try to insert comma where it's missing in the error region
        # Pattern: } or ] or " followed by whitespace and then { or [ or "
        error_region = re.sub(r'([}\]"])(\s+)([\[{"])', r'\1,\2\3', error_region)
        fixed = before_error + error_region + after_error
    
    # Global fixes for common patterns (conservative)
    # Fix missing comma between object properties (} followed by ")
    fixed = re.sub(r'\}(\s*")', r'},\1', fixed)
    
    # Fix missing comma between array elements (] followed by {)
    fixed = re.sub(r'\](\s*\{)', r'],\1', fixed)
    
    return fixed


def _parse_llm_response(response_content: str) -> Dict[str, Any]:
    """
    Parse LLM response and handle common JSON parsing errors.
    Logs the problematic JSON for debugging if parsing fails.
    """
    json_str = _extract_json_from_response(response_content)
    
    # First attempt: try parsing directly
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.warning(
            f"Initial JSON parsing failed at line {e.lineno}, column {e.colno}: {e.msg}. "
            f"Attempting to fix common issues..."
        )
        
        # Log the problematic section for debugging
        error_pos = e.pos if hasattr(e, 'pos') else None
        if error_pos:
            start = max(0, error_pos - 200)
            end = min(len(json_str), error_pos + 200)
            problematic_section = json_str[start:end]
            logger.debug(f"Problematic JSON section around error (pos {error_pos}): ...{problematic_section}...")
        
        # Attempt to fix common issues, passing error position for targeted fixes
        fixed_json = _fix_common_json_issues(json_str, error_pos)
        
        try:
            # Second attempt with fixed JSON
            data = json.loads(fixed_json)
            logger.info("Successfully parsed JSON after applying fixes")
        except json.JSONDecodeError as e2:
            # If still failing, log the full response for debugging
            logger.error(
                f"Failed to parse JSON even after fixes. Error at line {e2.lineno}, "
                f"column {e2.colno}: {e2.msg}. Full response length: {len(json_str)} chars"
            )
            logger.debug(f"Full JSON response (first 5000 chars): {json_str[:5000]}")
            logger.debug(f"Full JSON response (last 5000 chars): {json_str[-5000:]}")
            raise ValueError(
                f"Invalid JSON in LLM response. Parse error at line {e2.lineno}, "
                f"column {e2.colno}: {e2.msg}"
            ) from e2
    
    # Validate the parsed structure
    if not isinstance(data, dict):
        raise ValueError("Parsed JSON is not a dictionary")
    
    if "location" not in data:
        raise ValueError("Missing 'location' field in JSON response")
    
    if "sightseeing_places" not in data or not isinstance(data["sightseeing_places"], list):
        raise ValueError("Missing or invalid 'sightseeing_places' field in JSON response")

    return data

async def generate_travel_plan(travel_request: TravelRequest) -> TravelResponse:
    request_data = _get_request_data(travel_request)
    travel_chain = _get_travel_plan_generation_chain()
    response = await travel_chain.ainvoke(request_data)
    response_content = _parse_llm_response(response.content)
    logger.debug(f"response_content=\n{json.dumps(response_content,indent=4)}")
    return TravelResponse(**response_content)
