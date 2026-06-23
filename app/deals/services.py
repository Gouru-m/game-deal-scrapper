from app.extensions import db
from app.deals.models import Deal
from app.deals.scraper import scrape_source

def refresh_deals(source_key="demo_store", user_agent=None):
    scraped_deals = scrape_source(
        source_key=source_key,
        user_agent=user_agent or "GameDealsStudentProject/1.0"
    )
    
    Deal.query.delete()

    for item in scraped_deals:
        deal = Deal(**item)
        db.session.add(deal)

    db.session.commit()
    return len(scraped_deals)

def get_filtered_deals(genre=None, max_price=None, best_only=False): 
    query = Deal.query

    if genre:
        query = query.filter(Deal.genre == genre)

    if max_price is not None:
        query = query.filter(Deal.sale_price <= max_price)

    deals = query.order_by(Deal.discount_percent.desc().nullslast(), Deal.sale_price.asc()).all()

    if best_only:
        deals = [deal for deal in deals if deal.is_best_deal]

    return deals

def get_available_genres():
    rows = db.session.query(Deal.genre).distinct().order_by(Deal.genre).all()
    return [row[0] for row in rows if row[0]]