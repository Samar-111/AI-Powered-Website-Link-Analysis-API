import re
from typing import Dict, List, Any
import httpx
from bs4 import BeautifulSoup
from app.config import settings
from app.utils.validators import validate_and_sanitize_url

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
}

class ExtractedWebsiteData:
    def __init__(
        self,
        url: str,
        title: str,
        meta_description: str,
        meta_keywords: List[str],
        site_name: str,
        headings: List[str],
        cleaned_text: str,
        detected_links: List[str],
    ):
        self.url = url
        self.title = title
        self.meta_description = meta_description
        self.meta_keywords = meta_keywords
        self.site_name = site_name
        self.headings = headings
        self.cleaned_text = cleaned_text
        self.detected_links = detected_links

    def to_llm_context(self) -> str:
        parts = [
            f"TARGET WEBSITE: {self.url}",
            f"TITLE: {self.title}",
            f"SITE NAME: {self.site_name}",
            f"META DESCRIPTION: {self.meta_description}",
            f"META KEYWORDS: {', '.join(self.meta_keywords) if self.meta_keywords else 'None provided'}",
            f"KEY HEADINGS:\n" + "\n".join(f"- {h}" for h in self.headings[:25]),
            f"REPRESENTATIVE SITE LINKS:\n" + "\n".join(f"- {l}" for l in self.detected_links[:15]),
            f"EXTRACTED CONTENT SAMPLE:\n{self.cleaned_text}"
        ]
        return "\n\n".join(parts)

class WebsiteExtractor:
    def __init__(self, timeout: int = settings.TIMEOUT_SECONDS, max_chars: int = settings.MAX_EXTRACT_CHARS):
        self.timeout = timeout
        self.max_chars = max_chars

    async def fetch_html(self, url: str) -> str:
        sanitized_url = validate_and_sanitize_url(url)
        async with httpx.AsyncClient(
            headers=DEFAULT_HEADERS,
            timeout=self.timeout,
            follow_redirects=True,
            verify=False
        ) as client:
            try:
                response = await client.get(sanitized_url)
                if response.history:
                    for redirect_resp in response.history:
                        validate_and_sanitize_url(str(redirect_resp.url))
                validate_and_sanitize_url(str(response.url))
                response.raise_for_status()
                return response.text
            except httpx.HTTPStatusError as e:
                status = e.response.status_code
                if status == 404:
                    raise ValueError(f"Website returned 404 Not Found at '{sanitized_url}'.")
                elif status in (401, 403):
                    raise ValueError(f"Website access was denied ({status} Forbidden/Unauthorized) for '{sanitized_url}'.")
                elif status >= 500:
                    raise ValueError(f"Target website server error ({status}) when accessing '{sanitized_url}'.")
                else:
                    raise ValueError(f"Website returned HTTP {status} error for '{sanitized_url}'.")
            except httpx.ConnectTimeout:
                raise ValueError(f"Connection timed out while trying to reach '{sanitized_url}'.")
            except httpx.ReadTimeout:
                raise ValueError(f"Website took too long to respond (read timeout) at '{sanitized_url}'.")
            except httpx.ConnectError:
                raise ValueError(f"Could not connect to '{sanitized_url}'. Please check if the host is reachable.")
            except httpx.RequestError as e:
                raise ValueError(f"Network error while fetching '{sanitized_url}': {str(e)}")

    def extract_content(self, url: str, html: str) -> ExtractedWebsiteData:
        soup = BeautifulSoup(html, "html.parser")

        title = ""
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        og_title = soup.find("meta", property="og:title")
        if not title and og_title and og_title.get("content"):
            title = og_title.get("content").strip()

        meta_description = ""
        meta_desc_tag = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
        if meta_desc_tag and meta_desc_tag.get("content"):
            meta_description = meta_desc_tag.get("content").strip()
        else:
            og_desc = soup.find("meta", property="og:description")
            if og_desc and og_desc.get("content"):
                meta_description = og_desc.get("content").strip()

        meta_keywords = []
        meta_kw_tag = soup.find("meta", attrs={"name": re.compile(r"^keywords$", re.I)})
        if meta_kw_tag and meta_kw_tag.get("content"):
            raw_keywords = meta_kw_tag.get("content").split(",")
            meta_keywords = [kw.strip() for kw in raw_keywords if kw.strip()]

        site_name = ""
        og_site_name = soup.find("meta", property="og:site_name")
        if og_site_name and og_site_name.get("content"):
            site_name = og_site_name.get("content").strip()

        headings = []
        for tag_name in ("h1", "h2", "h3"):
            for h in soup.find_all(tag_name):
                text = h.get_text(separator=" ", strip=True)
                if text and len(text) > 2 and text not in headings:
                    headings.append(text)

        links = []
        for a in soup.find_all("a", href=True):
            href = a.get("href").strip()
            anchor_text = a.get_text(strip=True)
            if href and not href.startswith(("#", "javascript:", "mailto:", "tel:")):
                label = f"{anchor_text} ({href})" if anchor_text else href
                if label not in links:
                    links.append(label)

        for element in soup(["script", "style", "noscript", "svg", "canvas", "iframe", "form"]):
            element.decompose()

        body_tag = soup.body or soup
        raw_text = body_tag.get_text(separator=" ", strip=True)
        cleaned_text = re.sub(r"\s+", " ", raw_text).strip()

        if len(cleaned_text) > self.max_chars:
            cleaned_text = cleaned_text[:self.max_chars] + "... [TRUNCATED FOR TOKEN OPTIMIZATION]"

        return ExtractedWebsiteData(
            url=url,
            title=title,
            meta_description=meta_description,
            meta_keywords=meta_keywords,
            site_name=site_name,
            headings=headings,
            cleaned_text=cleaned_text,
            detected_links=links[:30],
        )

    async def extract_from_url(self, url: str) -> ExtractedWebsiteData:
        html = await self.fetch_html(url)
        return self.extract_content(url, html)
