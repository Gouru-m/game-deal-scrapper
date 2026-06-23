from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.deals.services import(
    get_filtered_deals,
    get_available_genres,
    refresh_deals,
)

deals_bp = Blueprint("deals", __name__)

@deals_bp.get("/")
def dashboard():
    genre = request.args.get("genre") or None
    max_price_raw = request.args.get("max_price") or None
    best_only = request.args.get("best_only") == "on"

    max_price = None 
    if max_price_raw:
        try:
            max_price = float(max_price_raw)
        except ValueError:
            flash("Invalid price filter.", "error")

    deals = get_filtered_deals(
        genre=genre,
        max_price=max_price,
        best_only=best_only,
    )
    genres = get_available_genres()

    return render_template(
        "deals/dashboard.html",
        deals=deals,
        genres=genres,
        selected_genre=genre,
        max_price=max_price_raw,
        best_only=best_only
    )

@deals_bp.post("/refresh")
def refresh():
    try:
        count = refresh_deals()
        flash(f"Scraped {count} deals successfully.", "success")
    except Exception:
        flash("Could not refresh deals. Please check the scraper/source.", "error")

    return redirect(url_for("deals.dashboard")) 