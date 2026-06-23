import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-this")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///game_deals.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #security settings for cookies/sessions
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    #only use secure cookies in prod with HTTPS
    SESSION_COOKIE_SECURE = os.environ.get("FLASK_ENV") == "production"

    #CSRF protection
    WTF_CSRF_ENABLED = True