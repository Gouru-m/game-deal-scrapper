import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

ALLOWED_SOURCES = {
    "demo-store" : "https://example.com/game-deals"
}

class ScraperError(Exception):
    pass

def fetch_html(url, user_agent="GameDealsStudentProject/1.0" ):
    headers = {
    "User-Agent": user_agent
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as exc:
        raise ScraperError(f"Could not fetch page: {exc}") from exc
    
def parse_deals(html, base_url, source_name):
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

        original_price = None
        if original_price_el:
             original_price = clean_price(original_price_el.get_text(strip=True))
  
        discount = calculate_discount(original_price, sale_price)

        product_url = base_url
        if link_el and link_el.get("href"):
            product_url = urljoin(base_url, link_el["href"])

        image_url = None
        if image_el and image_el.get("src"):
            image_url = urljoin(base_url, image_el["src"])

        deals.append({
            "title" : title,
            "genre" : genre_el.get_text(strip=True) if genre_el else "Unknown",
            "original_price" : original_price,
            "sale_price" : sale_price,
            "discount_percent" :discount,
            "source" : source_name,
            "product_url" : product_url,
            "image_url" : image_url,
        })

    return deals

def clean_price(raw_price):
    cleaned = (
        raw_price.replace("$", "")
        .replace("Rs £", "")
        .replace("£", "")
        .replace(",", "")
        .strip
    )
    return float(cleaned)

def calculate_discount(original_price, sale_price):
    if not original_price or original_price <= sale_price:
        return None
    return round(((original_price - sale_price) / original_price) * 100)

def scrape_source(source_key, user_agent ="GameDealsStudentProject/1.0"):
    if source_key not in ALLOWED_SOURCES:
        raise ScraperError("Scraping source is not allowed.")
    
    url = ALLOWED_SOURCES[source_key]
    html = fetch_html(url, user_agent=user_agent)

    #polite delay to avoid hammer the website
    time.sleep(1) 
    return parse_deals(html, base_url=url, source_name=source_key)