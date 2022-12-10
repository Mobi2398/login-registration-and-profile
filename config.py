"""Configuration Class for Flask"""
import os
import secrets


class Config:
    """Default Config Settings"""
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', "TRUE")
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', "sqlite:///app.db")
    SECRET_KEY = secrets.token_urlsafe(16)
