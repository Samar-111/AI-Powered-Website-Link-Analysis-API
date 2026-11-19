from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class LinkAnalysisRequest(BaseModel):
    url: str = Field(..., description="The website URL to analyze", json_schema_extra={"example": "https://stripe.com"})

class BrandInfo(BaseModel):
    name: str = Field(..., description="Brand or company name")
    category: str = Field(..., description="Main business category")
    summary: str = Field(..., description="Concise business summary")
    main_products_and_services: List[str] = Field(default_factory=list)

class CompetitorItem(BaseModel):
    brand_name: str
    main_service: str
    target_market: str
    key_strength: str
    weaknesses_or_gaps: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    opportunity: str

class ComparisonMatrixRow(BaseModel):
    aspect: str
    your_brand: str
    competitor: str

class CompetitorAnalysisSection(BaseModel):
    brand_overview: str
    main_business_category: str
    main_products_and_services: List[str] = Field(default_factory=list)
    competitors: List[CompetitorItem] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    weaknesses_or_gaps: List[str] = Field(default_factory=list)
    opportunities: List[str] = Field(default_factory=list)
    comparison_matrix: List[ComparisonMatrixRow] = Field(default_factory=list)

class TargetSearchQueryItem(BaseModel):
    query: str
    platforms: List[str]
    intent: str
    business_relevance: str
    target_audience: str

class KeywordRecommendations(BaseModel):
    primary_keyword: str
    secondary_keywords: List[str] = Field(default_factory=list)
    long_tail_keywords: List[str] = Field(default_factory=list)
    relevant_business_keywords: List[str] = Field(default_factory=list)

class TitleRecommendation(BaseModel):
    recommended_title: str
    primary_keyword: str
    improved_structure: str

class MetaDescriptionRecommendation(BaseModel):
    recommended_meta_description: str
    short_summary: str
    relevant_keywords: List[str] = Field(default_factory=list)

class SeoImprovementsSection(BaseModel):
    primary_keyword: str
    secondary_keywords: List[str] = Field(default_factory=list)
    long_tail_keywords: List[str] = Field(default_factory=list)
    relevant_business_keywords: List[str] = Field(default_factory=list)
    recommended_title: str
    title_details: Optional[TitleRecommendation] = None
    meta_description: str
    meta_description_details: Optional[MetaDescriptionRecommendation] = None
    supporting_content: List[str] = Field(default_factory=list)

class ServiceItem(BaseModel):
    service_name: str
    description: str
    target_industry: str
    target_customer: str
    main_benefit: str
    is_inferred: bool = False
    source: str = "extracted"

class AudienceProfile(BaseModel):
    audience_name: str
    business_type: str
    requirement: str

class TargetAudienceSection(BaseModel):
    primary_audience: List[str] = Field(default_factory=list)
    secondary_audience: List[str] = Field(default_factory=list)
    industries: List[str] = Field(default_factory=list)
    business_types: List[str] = Field(default_factory=list)
    customer_profiles: List[AudienceProfile] = Field(default_factory=list)
    location_focus: Optional[str] = "Global / Not explicitly restricted"
    customer_needs: List[str] = Field(default_factory=list)
    customer_challenges: List[str] = Field(default_factory=list)
    potential_customer_interests: List[str] = Field(default_factory=list)
    recommended_marketing_segments: List[str] = Field(default_factory=list)

class AnalysisData(BaseModel):
    competitor_analysis: CompetitorAnalysisSection
    target_search_queries: List[TargetSearchQueryItem]
    seo_improvements: SeoImprovementsSection
    top_services: List[ServiceItem]
    target_audience: TargetAudienceSection

class LinkAnalysisResponse(BaseModel):
    success: bool = True
    website: str
    brand: BrandInfo
    analysis: AnalysisData
    metadata: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    success: bool = False
    website: Optional[str] = None
    error: str
    detail: Optional[str] = None
