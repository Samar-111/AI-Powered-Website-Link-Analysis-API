import time
from typing import Dict, Tuple, Optional
from app.config import settings
from app.schemas import LinkAnalysisResponse
from app.services.website_extractor import WebsiteExtractor
from app.services.llm_service import LLMService
from app.services.competitor_service import CompetitorService
from app.utils.validators import validate_and_sanitize_url

class AnalysisService:
    def __init__(self):
        self.extractor = WebsiteExtractor()
        self.llm = LLMService()
        self._cache: Dict[str, Tuple[float, LinkAnalysisResponse]] = {}
        self.cache_ttl = settings.CACHE_TTL_SECONDS

    def _get_from_cache(self, url: str) -> Optional[LinkAnalysisResponse]:
        if url in self._cache:
            cached_time, response = self._cache[url]
            if time.time() - cached_time < self.cache_ttl:
                return response
            else:
                del self._cache[url]
        return None

    def _save_to_cache(self, url: str, response: LinkAnalysisResponse) -> None:
        self._cache[url] = (time.time(), response)

    async def run_analysis(self, raw_url: str) -> LinkAnalysisResponse:
        validated_url = validate_and_sanitize_url(raw_url)

        cached = self._get_from_cache(validated_url)
        if cached:
            return cached

        extracted_data = await self.extractor.extract_from_url(validated_url)
        llm_context = extracted_data.to_llm_context()

        brand, analysis, metadata = await self.llm.analyze_website_content(
            url=validated_url,
            context=llm_context
        )

        analysis.competitor_analysis = CompetitorService.ensure_competitor_integrity(
            brand=brand,
            competitor_section=analysis.competitor_analysis
        )

        if not brand.name or brand.name.lower() in ("unknown", "string"):
            brand.name = extracted_data.site_name or extracted_data.title or "Identified Brand"

        response = LinkAnalysisResponse(
            success=True,
            website=validated_url,
            brand=brand,
            analysis=analysis,
            metadata=metadata
        )

        self._save_to_cache(validated_url, response)
        return response

analysis_service = AnalysisService()
