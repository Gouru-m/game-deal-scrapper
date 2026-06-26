from app import create_app
from app.extensions import db
from app.deals.models import Deal
from app.deals.services import get_filtered_deals

class TestConfig:
    SECRET_KEY ="test-secret-key"
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

def test_filter_deals_by_genre_and_price():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()

        db.session.add(
            Deal(
                title="Action Game",
                genre="Action",
                original_price=50,
                sale_price=10,
                discount_percent=80,
                source="test",
                product_url="https://example.com/action"
            )
        )

        db.session.add(
            Deal(
                title="RPG Game",
                genre="RPG",
                original_price=60,
                sale_price=30,
                discount_percent=50,
                source="test",
                product_url="https://example.com/rpg"
            )
        )

        db.session.commit()

        results = get_filtered_deals(genre="Action", max_price=20, best_only=False)

        assert len(results) == 1
        assert results[0].title == "Action Game"