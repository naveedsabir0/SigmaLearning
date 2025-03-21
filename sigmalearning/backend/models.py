from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from datetime import datetime
from sqlalchemy import text

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    # Additional profile fields:
    home_address = db.Column(db.String(200), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    region = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    profile_pic = db.Column(db.Text, nullable=True)  # Stored as a base64 string

    # New fields for email verification:
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    verification_token = db.Column(db.String(100), nullable=True)
    
    # New fields for password reset:
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)

    # Two-factor authentication fields:
    two_fa_enabled = db.Column(db.Boolean, default=False, nullable=False, server_default=text("0"))
    activation_2fa_code = db.Column(db.String(6), nullable=True)
    activation_2fa_expiry = db.Column(db.DateTime, nullable=True)
    login_2fa_code = db.Column(db.String(6), nullable=True)
    login_2fa_expiry = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.Column(db.Text, nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(50), unique=True, nullable=False)  # Unique identifier like "course1"
    title = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)  # Path to the course file (e.g., video)
    description = db.Column(db.Text, nullable=True)
    difficulty = db.Column(db.String(50), nullable=True)