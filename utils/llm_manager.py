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

    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", response_text, re.DOTALL)
    if match:
        return match.group(1).strip()

    match = re.search(r"\{.*\}", response_text, re.DOTALL)
    if match:
        return match.group(0).strip()

    return response_text.strip()


def _parse_llm_response(response_content: str) -> Dict[str, Any]:
    json_str = _extract_json_from_response(response_content)
    data = json.loads(json_str)

    if not isinstance(data, dict) or "location" not in data or not isinstance(data["sightseeing_places"], list):
        raise ValueError("Invalid JSON structure")

    return data

async def generate_travel_plan(travel_request: TravelRequest) -> TravelResponse:
    request_data = _get_request_data(travel_request)
    travel_chain = _get_travel_plan_generation_chain()
    response = await travel_chain.ainvoke(request_data)
    response_content = _parse_llm_response(response.content)
    return TravelResponse(**response_content)
