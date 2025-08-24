import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:050820@localhost:5432/fyyur"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev_secret_key_change_me"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
