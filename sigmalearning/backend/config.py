import os
from flask_mail import Mail

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key")  # Store this in .env for security

    # Flask-Mail Configuration
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")  # Set in .env
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")  # Set in .env
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME")

mail = Mail()