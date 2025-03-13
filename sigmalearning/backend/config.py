import os
from flask_mail import Mail

# Define the base directory for the backend folder
basedir = os.path.abspath(os.path.dirname(__file__))  # Set the base directory for the app

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "instance", "database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key")  # Store in .env for security
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limit payload to 16 MB for large uploads
    
    # Flask-Mail Configuration
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")  # Set in .env
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")  # Set in .env
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME")

mail = Mail()
