from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.deals.services import(
    get_filtered_deals,
    get_available_genres,
    refresh_deals,
)
from app.deals.forms import FilterForm, RefreshDealsForm
from app.deals.scraper import ScraperError
from app.extensions import limiter

deals_bp = Blueprint("deals", __name__)

@deals_bp.get("/")
def dashboard():
    genres = get_available_genres()

    form = FilterForm(
        request.args,
        genres=genres
    )
    max_price = None
    genre = None
    best_only = False

    if form.validate():
        genre = form.genre.data or None
        best_only = form.best_only.data

        if form.max_price.data is not None:
            max_price = float(form.max_price.data)
        else:
            flash("Some filters were invalid and have been ignored.", "error")

    deals = get_filtered_deals(
        genre=genre,
        max_price=max_price,
        best_only=best_only,
    )

    refresh_form = RefreshDealsForm()

    return render_template(
        "deals/dashboard.html",
        form=form,
        deals=deals,
        refresh_form=refresh_form
    )

@deals_bp.post("/refresh")
@limiter.limit("5 per minute")
def refresh():
    form = RefreshDealsForm()

    if not form.validate_on_submit():
        flash("Invalid refresh request.", "error")
        return redirect(url_for("deals.dashboard"))

    try:
        count = refresh_deals(
            source_key="demo_store",
            user_agent=current_app.config["SCRAPER_USER_AGENT"]
        )
        flash(f"Successfully refreshed {count} deals.", "success")
    except ScraperError:
        flash("Could not scrape deals from the selected source.", "error")
    except Exception:
        flash("Could not refresh deals. Please check the scraper/source.", "error")

    return redirect(url_for("deals.dashboard")) 