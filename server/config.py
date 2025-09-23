# server/config.py

import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "cartandshop")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///cartify.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
