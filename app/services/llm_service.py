import asyncio
import json
import os
import re
import time
from typing import Dict, Any, Tuple
from google import genai
from app.config import settings
from app.schemas import (
    BrandInfo,
    AnalysisData,
    CompetitorAnalysisSection,
    CompetitorItem,
    ComparisonMatrixRow,
    TargetSearchQueryItem,
    SeoImprovementsSection,
    TitleRecommendation,
    MetaDescriptionRecommendation,
    ServiceItem,
    TargetAudienceSection,
    AudienceProfile,
    LinkAnalysisResponse,
)

SYSTEM_PROMPT = """You are an elite enterprise business strategist, digital marketer, and technical SEO analyst.
Your task is to analyze website content and extract comprehensive, high-accuracy intelligence across five distinct areas:
1. Competitor vs Your Brand Details (identify at least 3 direct or category competitors, compare strengths/weaknesses/positioning).
2. Top 5 Target Search Queries (across Google, Facebook, Instagram, LinkedIn, and X with explicit search intent; DO NOT invent fake search volume numbers).
3. Practical SEO Improvements (primary/secondary/long-tail keywords, title recommendation, meta description, and 5+ supporting content topics).
4. Top 5 Core Services (service name, description, target industry, customer, main benefit, and boolean flag if inferred).
5. Target Audience Identification (primary/secondary segments, industry segments, business types, customer profiles, needs, challenges, and marketing segments).

You MUST strictly output valid JSON adhering to the exact JSON schema requested. Do not include markdown code block syntax if possible, or provide raw JSON."""

USER_PROMPT_TEMPLATE = """Analyze the following website data and generate structured intelligence.

WEBSITE DATA:
{context}

Respond ONLY with a valid JSON object strictly adhering to this structure:
{{
  "brand": {{
    "name": "string",
    "category": "string",
    "summary": "string",
    "main_products_and_services": ["string", "string"]
  }},
  "analysis": {{
    "competitor_analysis": {{
      "brand_overview": "string",
      "main_business_category": "string",
      "main_products_and_services": ["string"],
      "competitors": [
        {{
          "brand_name": "string",
          "main_service": "string",
          "target_market": "string",
          "key_strength": "string",
          "weaknesses_or_gaps": ["string"],
          "strengths": ["string"],
          "opportunity": "string"
        }}
      ],
      "strengths": ["string"],
      "weaknesses_or_gaps": ["string"],
      "opportunities": ["string"],
      "comparison_matrix": [
        {{
          "aspect": "string",
          "your_brand": "string",
          "competitor": "string"
        }}
      ]
    }},
    "target_search_queries": [
      {{
        "query": "string",
        "platforms": ["Google", "LinkedIn"],
        "intent": "string",
        "business_relevance": "string",
        "target_audience": "string"
      }}
    ],
    "seo_improvements": {{
      "primary_keyword": "string",
      "secondary_keywords": ["string"],
      "long_tail_keywords": ["string"],
      "relevant_business_keywords": ["string"],
      "recommended_title": "string",
      "title_details": {{
        "recommended_title": "string",
        "primary_keyword": "string",
        "improved_structure": "string"
      }},
      "meta_description": "string",
      "meta_description_details": {{
        "recommended_meta_description": "string",
        "short_summary": "string",
        "relevant_keywords": ["string"]
      }},
      "supporting_content": ["string"]
    }},
    "top_services": [
      {{
        "service_name": "string",
        "description": "string",
        "target_industry": "string",
        "target_customer": "string",
        "main_benefit": "string",
        "is_inferred": false,
        "source": "extracted"
      }}
    ],
    "target_audience": {{
      "primary_audience": ["string"],
      "secondary_audience": ["string"],
      "industries": ["string"],
      "business_types": ["string"],
      "customer_profiles": [
        {{
          "audience_name": "string",
          "business_type": "string",
          "requirement": "string"
        }}
      ],
      "location_focus": "string",
      "customer_needs": ["string"],
      "customer_challenges": ["string"],
      "potential_customer_interests": ["string"],
      "recommended_marketing_segments": ["string"]
    }}
  }}
}}

Ensure:
- Minimum 3 realistic competitors are identified.
- Exactly 5 top target search queries mapped across Google, Facebook, Instagram, LinkedIn, or X.
- Exactly 5 top services.
- Ground all facts in the extracted website text wherever possible."""

class LLMService:
    def __init__(self, api_key: str = "", model: str = ""):
        self._api_key = api_key
        self._model = model
        self._client = None

    def _resolve_api_key(self) -> str:
        key = self._api_key or os.getenv("GEMINI_API_KEY", "") or settings.GEMINI_API_KEY
        return key.strip().strip('"').strip("'")

    def _resolve_model(self) -> str:
        return self._model or os.getenv("GEMINI_MODEL", "") or settings.GEMINI_MODEL

    def _get_client(self) -> genai.Client:
        key = self._resolve_api_key()
        if not key:
            raise ValueError("GEMINI_API_KEY is not configured in environment or .env file.")
        if self._client is None or getattr(self, "_active_key", "") != key:
            self._client = genai.Client(api_key=key)
            self._active_key = key
        return self._client

    def _clean_json_response(self, text: str) -> str:
        text = text.strip()
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
        if match:
            return match.group(1).strip()
        return text

    async def analyze_website_content(self, url: str, context: str) -> Tuple[BrandInfo, AnalysisData, Dict[str, Any]]:
        client = self._get_client()
        model = self._resolve_model()
        prompt = USER_PROMPT_TEMPLATE.format(context=context)
        start_time = time.perf_counter()

        try:
            response = await asyncio.to_thread(
                client.models.generate_content,
                model=model,
                contents=prompt,
                config={
                    "system_instruction": SYSTEM_PROMPT,
                    "temperature": 0.2,
                    "response_mime_type": "application/json"
                }
            )
        except Exception as e:
            raise ValueError(f"LLM API returned error: {str(e)}")

        elapsed = round(time.perf_counter() - start_time, 3)
        raw_text = response.text or ""
        cleaned_json = self._clean_json_response(raw_text)

        try:
            parsed_data = json.loads(cleaned_json)
        except json.JSONDecodeError as e:
            raise ValueError(f"Could not parse LLM output as JSON: {str(e)}. Raw text: {raw_text[:200]}")

        usage = response.usage_metadata
        prompt_tokens = getattr(usage, "prompt_token_count", 0) if usage else 0
        completion_tokens = getattr(usage, "candidates_token_count", 0) if usage else 0
        total_tokens = getattr(usage, "total_token_count", 0) if usage else 0

        metadata = {
            "model_used": model,
            "response_time_seconds": elapsed,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
        }

        brand_dict = parsed_data.get("brand", {})
        analysis_dict = parsed_data.get("analysis", {})

        brand = BrandInfo(**brand_dict)
        analysis = AnalysisData(**analysis_dict)

        return brand, analysis, metadata
