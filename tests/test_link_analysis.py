import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from app.main import app
from app.utils.validators import validate_and_sanitize_url
from app.services.website_extractor import WebsiteExtractor
from app.services.analysis_service import analysis_service
from app.schemas import (
    BrandInfo,
    AnalysisData,
    CompetitorAnalysisSection,
    CompetitorItem,
    ComparisonMatrixRow,
    TargetSearchQueryItem,
    SeoImprovementsSection,
    ServiceItem,
    TargetAudienceSection,
    AudienceProfile,
)

client = TestClient(app)

def test_url_validator_valid():
    assert validate_and_sanitize_url("example.com", check_dns=False) == "https://example.com"
    assert validate_and_sanitize_url("https://example.com", check_dns=False) == "https://example.com"

def test_url_validator_with_mocked_dns():
    with patch("socket.getaddrinfo", return_value=[(None, None, None, None, ("93.184.216.34", 80))]):
        assert validate_and_sanitize_url("https://example.com", check_dns=True) == "https://example.com"

def test_url_validator_invalid_schemes():
    with pytest.raises(ValueError):
        validate_and_sanitize_url("ftp://example.com", check_dns=False)
    with pytest.raises(ValueError):
        validate_and_sanitize_url("", check_dns=False)

def test_ssrf_prevention_local_ips():
    with pytest.raises(ValueError):
        validate_and_sanitize_url("http://127.0.0.1:8000", check_dns=False)
    with pytest.raises(ValueError):
        validate_and_sanitize_url("http://localhost:4000", check_dns=False)
    with pytest.raises(ValueError):
        validate_and_sanitize_url("http://169.254.169.254/latest/meta-data", check_dns=False)

def test_ssrf_prevention_private_dns():
    with patch("socket.getaddrinfo", return_value=[(None, None, None, None, ("192.168.1.100", 80))]):
        with pytest.raises(ValueError):
            validate_and_sanitize_url("https://internal.corp", check_dns=True)

def test_html_content_extraction():
    sample_html = """
    <!DOCTYPE html>
    <html>
      <head>
        <title>Nova Cloud - NextGen Cloud Hosting</title>
        <meta name="description" content="High performance managed cloud hosting for modern web applications.">
        <meta name="keywords" content="cloud, hosting, kubernetes, vps">
      </head>
      <body>
        <h1>Deploy Faster with Nova Cloud</h1>
        <h2>Enterprise Cloud Solutions</h2>
        <p>Nova Cloud delivers zero-downtime infrastructure and developer-friendly servers.</p>
        <a href="/pricing">View Pricing</a>
        <script>console.log('should be stripped');</script>
        <style>body { color: red; }</style>
      </body>
    </html>
    """
    extractor = WebsiteExtractor()
    extracted = extractor.extract_content("https://novacloud.io", sample_html)

    assert extracted.title == "Nova Cloud - NextGen Cloud Hosting"
    assert extracted.meta_description == "High performance managed cloud hosting for modern web applications."
    assert "cloud" in extracted.meta_keywords
    assert "Deploy Faster with Nova Cloud" in extracted.headings
    assert "Enterprise Cloud Solutions" in extracted.headings
    assert "zero-downtime" in extracted.cleaned_text
    assert "should be stripped" not in extracted.cleaned_text

def test_api_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert "endpoints" in data

def test_api_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_api_link_analysis_ssrf_block():
    response = client.post("/link-analysis", json={"url": "http://127.0.0.1:4000"})
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data or "error" in data

def test_full_analysis_pipeline_mocked():
    mock_brand = BrandInfo(
        name="Nova Cloud",
        category="Cloud Computing & Infrastructure",
        summary="NextGen high performance managed cloud hosting.",
        main_products_and_services=["Managed Kubernetes", "High Performance VPS"]
    )

    mock_analysis = AnalysisData(
        competitor_analysis=CompetitorAnalysisSection(
            brand_overview="Nova Cloud provides developer-first cloud servers.",
            main_business_category="Cloud Infrastructure",
            main_products_and_services=["Managed Cloud", "VPS"],
            competitors=[
                CompetitorItem(
                    brand_name="DigitalOcean",
                    main_service="Cloud Droplets",
                    target_market="Developers & Startups",
                    key_strength="Simplicity and developer community",
                    weaknesses_or_gaps=["Higher costs for enterprise scaling"],
                    strengths=["Strong brand loyalty"],
                    opportunity="Offer competitive bare metal pricing"
                ),
                CompetitorItem(
                    brand_name="AWS Lightsail",
                    main_service="VPS & Containers",
                    target_market="SMBs and AWS customers",
                    key_strength="AWS ecosystem integration",
                    weaknesses_or_gaps=["Complex pricing over time"],
                    strengths=["Global data centers"],
                    opportunity="Provide transparent flat pricing"
                ),
                CompetitorItem(
                    brand_name="Linode (Akamai)",
                    main_service="Compute Instances",
                    target_market="Linux Sysadmins & Developers",
                    key_strength="Performance and Akamai edge",
                    weaknesses_or_gaps=["Legacy interface"],
                    strengths=["Affordable bandwidth"],
                    opportunity="Deliver modern unified dashboard"
                )
            ],
            strengths=["Zero latency edge network", "Predictable flat pricing"],
            weaknesses_or_gaps=["Newer market entrant"],
            opportunities=["Capture developers fleeing complex hyperscalers"],
            comparison_matrix=[
                ComparisonMatrixRow(
                    aspect="Brand Name",
                    your_brand="Nova Cloud",
                    competitor="DigitalOcean"
                )
            ]
        ),
        target_search_queries=[
            TargetSearchQueryItem(
                query="Best developer friendly cloud hosting",
                platforms=["Google", "LinkedIn"],
                intent="Service Search",
                business_relevance="Direct lead generation for hosting",
                target_audience="CTOs & DevOps Engineers"
            ),
            TargetSearchQueryItem(
                query="Affordable managed kubernetes for startups",
                platforms=["Google", "X"],
                intent="High Intent Commercial",
                business_relevance="Acquires tech founders",
                target_audience="Startup Founders"
            ),
            TargetSearchQueryItem(
                query="DigitalOcean alternatives 2026",
                platforms=["Google", "LinkedIn"],
                intent="Competitor Comparison",
                business_relevance="Captures switching customers",
                target_audience="Software Engineers"
            ),
            TargetSearchQueryItem(
                query="Fastest VPS server hosting benchmarks",
                platforms=["X", "LinkedIn"],
                intent="Research & Discovery",
                business_relevance="Showcases raw performance",
                target_audience="System Administrators"
            ),
            TargetSearchQueryItem(
                query="Cloud hosting discount code",
                platforms=["Instagram", "Facebook"],
                intent="Discount Discovery",
                business_relevance="Broad consumer discovery",
                target_audience="Indie Hackers"
            )
        ],
        seo_improvements=SeoImprovementsSection(
            primary_keyword="Cloud Hosting",
            secondary_keywords=["Managed VPS", "Cloud Servers", "Kubernetes"],
            long_tail_keywords=["high performance managed cloud hosting for developers"],
            relevant_business_keywords=["vps", "compute", "cloud infrastructure"],
            recommended_title="Nova Cloud | High-Performance Managed Cloud Hosting",
            meta_description="Deploy scalable cloud instances in seconds with Nova Cloud. Enjoy 99.99% uptime and flat monthly pricing.",
            supporting_content=["Managed Kubernetes Landing Page", "VPS Migration Guide", "AWS vs Nova Cloud Cost Comparison"]
        ),
        top_services=[
            ServiceItem(
                service_name="Managed Cloud VPS",
                description="High frequency NVMe cloud instances.",
                target_industry="Software & IT",
                target_customer="DevOps & Engineers",
                main_benefit="Blazing fast response times",
                is_inferred=False,
                source="extracted"
            ),
            ServiceItem(
                service_name="Kubernetes Engine",
                description="Automated container cluster deployment.",
                target_industry="Tech Startups",
                target_customer="Cloud Architects",
                main_benefit="Effortless autoscaling",
                is_inferred=False,
                source="extracted"
            ),
            ServiceItem(
                service_name="Global Object Storage",
                description="S3-compatible distributed object storage.",
                target_industry="Media & SaaS",
                target_customer="Backend Developers",
                main_benefit="Unlimited affordable data storage",
                is_inferred=True,
                source="inferred recommendation"
            ),
            ServiceItem(
                service_name="DDoS Protected Load Balancers",
                description="High throughput traffic distribution.",
                target_industry="Fintech & E-Commerce",
                target_customer="Security Leads",
                main_benefit="Enterprise resilience",
                is_inferred=False,
                source="extracted"
            ),
            ServiceItem(
                service_name="Database Clusters",
                description="Automated managed PostgreSQL and MySQL.",
                target_industry="Web Applications",
                target_customer="Full-stack Developers",
                main_benefit="Zero maintenance database operations",
                is_inferred=True,
                source="inferred recommendation"
            )
        ],
        target_audience=TargetAudienceSection(
            primary_audience=["Software Engineers", "DevOps Specialists", "Tech Founders"],
            secondary_audience=["Digital Agencies", "E-commerce Operators"],
            industries=["Information Technology", "SaaS", "Financial Technology"],
            business_types=["B2B SaaS", "Tech Startups", "Mid-sized Enterprises"],
            customer_profiles=[
                AudienceProfile(
                    audience_name="Startup CTO",
                    business_type="Fast Growing SaaS",
                    requirement="Predictable cloud costs and zero downtime"
                )
            ],
            location_focus="Global",
            customer_needs=["Fast compute instances", "Transparent pricing", "Easy API access"],
            customer_challenges=["Unexpected cloud bills from AWS", "Complex orchestration overhead"],
            potential_customer_interests=["Microservices", "DevOps automation", "Open source"],
            recommended_marketing_segments=["Cloud Cost Conscious Tech Founders", "Independent Developers"]
        )
    )

    with patch("socket.getaddrinfo", return_value=[(None, None, None, None, ("93.184.216.34", 80))]), \
         patch.object(WebsiteExtractor, "extract_from_url", new_callable=AsyncMock) as mock_extract, \
         patch.object(analysis_service.llm, "analyze_website_content", new_callable=AsyncMock) as mock_llm:

        mock_extract.return_value = WebsiteExtractor().extract_content(
            "https://novacloud.io",
            "<html><head><title>Nova Cloud</title></head><body><h1>Cloud</h1></body></html>"
        )
        mock_llm.return_value = (mock_brand, mock_analysis, {"prompt_tokens": 120, "completion_tokens": 400})

        res = client.post("/link-analysis", json={"url": "https://novacloud.io"})
        assert res.status_code == 200
        payload = res.json()
        assert payload["success"] is True
        assert payload["website"] == "https://novacloud.io"
        assert payload["brand"]["name"] == "Nova Cloud"
        assert len(payload["analysis"]["competitor_analysis"]["competitors"]) >= 3
        assert len(payload["analysis"]["target_search_queries"]) == 5
        assert len(payload["analysis"]["top_services"]) == 5
        assert len(payload["analysis"]["target_audience"]["primary_audience"]) > 0
