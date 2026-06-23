from datetime import datetime, UTC
from app.extensions import db

class Deal(db.Model):
    __tablename__ = "deals"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    genre = db.Column(db.String(80), nullable=True, index=True)
    original_price = db.Column(db.Float, nullable=True)
    sale_price = db.Column(db.Float, nullable=False, index=True)
    discount_percent = db.Column(db.Integer, nullable=True)
    source = db.Column(db.String(100), nullable=False)
    product_url = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    scraped_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), nullable=False)

    @property
    def is_best_deal(self):
        return(
            self.discount_percent is not None
            and self.discount_percent >= 50
        ) or self.sale_price <= 10