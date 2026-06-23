import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "GameDealsStudentProject/1.0 contact: your-email@example.com"
}

ALLOWED_SOURCES = {
    "demo-store" : "https://example.com/game-deals"
}

class ScraperError(Exception):
    pass

def fetch_html(url: str) -> str:
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as exc:
        raise ScraperError(f"Could not fetch page: {exc}") from exc
    
def parse_deals(html: str, base_url: str, source_name: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    deals = []

    for card in soup.select(".game-card"):
        title_el = card.select_one(".game-title")
        sale_price_el = card.select_one(".sale-price")
        original_price_el = card.select_one(".original-price")
        genre_el = card.select_one(".genre")
        link_el = card.select_one("a")
        image_el = card.select_one("img")

        if not title_el or not sale_price_el:
            continue

        title = title_el.get_text(strip=True)
        sale_price = clean_price(sale_price_el.get_text(strip=True))
        original_price = (
            clean_price(original_price_el.get_text(strip=True))
            if original_price_el else None
        )

        discount = calculate_discount(original_price, sale_price)

        deals.append({
            "title" : title,
            "genre" : genre_el.get_text(strip=True),
            "original_price" : original_price,
            "sale_price" : sale_price,
            "discount_price" :discount,
            "source" : source_name,
            "product_url" : urljoin(base_url, link_el["href"]) if link_el else base_url,
            "image_url" : urljoin(base_url, image_el["src"]) if image_el else None,
        })

    return deals

def clean_price(raw_price : str) -> float:
    cleaned = (
        raw_price.replace("$", "")
        .replace("Rs", "")
        .replace(",", "")
        .strip
    )
    return float(cleaned)

def calculate_discount(original_price: float | None, sale_price: float) -> int | None:
    if not original_price or original_price <= sale_price:
        return None
    return round(((original_price - sale_price) / original_price) * 100)

def scrape_source(source_key: str) -> list[dict]:
    if source_key not in ALLOWED_SOURCES:
        raise ScraperError("Source is not allowed.")
    
    url = ALLOWED_SOURCES[source_key]
    html = fetch_html(url)

    time.sleep(1) 
    return parse_deals(html, base_url=url, source_name=source_key)