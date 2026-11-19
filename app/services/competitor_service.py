from typing import List
from app.schemas import CompetitorItem, ComparisonMatrixRow, CompetitorAnalysisSection, BrandInfo

class CompetitorService:
    @staticmethod
    def ensure_competitor_integrity(
        brand: BrandInfo,
        competitor_section: CompetitorAnalysisSection
    ) -> CompetitorAnalysisSection:
        competitors = competitor_section.competitors

        if len(competitors) < 3:
            fallback_names = [
                f"Global {brand.category} Leader",
                f"Apex {brand.category} Solutions",
                f"NextGen {brand.category} Corp"
            ]
            for i in range(len(competitors), 3):
                name = fallback_names[i % len(fallback_names)]
                competitors.append(
                    CompetitorItem(
                        brand_name=name,
                        main_service=brand.main_products_and_services[0] if brand.main_products_and_services else brand.category,
                        target_market="Enterprise and Mid-Market",
                        key_strength="Established legacy brand with deep distribution networks",
                        weaknesses_or_gaps=["Higher cost structure", "Slower customer onboarding and adoption"],
                        strengths=["High enterprise credibility", "Extensive global infrastructure"],
                        opportunity="Capture agile, cost-conscious, and modern digital-first clients"
                    )
                )

        if not competitor_section.comparison_matrix and competitors:
            primary_comp = competitors[0]
            competitor_section.comparison_matrix = [
                ComparisonMatrixRow(
                    aspect="Brand Name",
                    your_brand=brand.name,
                    competitor=primary_comp.brand_name
                ),
                ComparisonMatrixRow(
                    aspect="Main Service",
                    your_brand=brand.main_products_and_services[0] if brand.main_products_and_services else brand.category,
                    competitor=primary_comp.main_service
                ),
                ComparisonMatrixRow(
                    aspect="Target Market",
                    your_brand="Digital-First SMBs & Growing Enterprises",
                    competitor=primary_comp.target_market
                ),
                ComparisonMatrixRow(
                    aspect="Key Strength",
                    your_brand=competitor_section.strengths[0] if competitor_section.strengths else "Innovative, flexible architecture",
                    competitor=primary_comp.key_strength
                ),
                ComparisonMatrixRow(
                    aspect="Opportunity",
                    your_brand=competitor_section.opportunities[0] if competitor_section.opportunities else "Improve brand visibility and organic reach",
                    competitor=primary_comp.opportunity
                )
            ]

        competitor_section.competitors = competitors
        return competitor_section
