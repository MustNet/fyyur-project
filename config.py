# config.py
import os
from urllib.parse import quote_plus

class Config:
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = quote_plus(os.getenv("DB_PASS", ""))  # URL-sicher, falls Sonderzeichen
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "fyyur")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key_change_me")
