from flask import Blueprint, request, jsonify, url_for, current_app
from flask_jwt_extended import create_access_token
from models import db, User
from werkzeug.security import generate_password_hash
import secrets
from flask_mail import Message
from config import mail
from datetime import datetime, timedelta

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not all(k in data for k in ["username", "email", "password"]):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400

    try:
        user = User(username=data['username'], email=data['email'])
        user.set_password(data['password'])  # Hash and set the password
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))  # Convert to string
        return jsonify({"message": "Login successful", "access_token": access_token})
    else:
        return jsonify({"message": "Invalid credentials"}), 401
# @auth_bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')

#     user = User.query.filter_by(username=username).first()

#     if user and user.check_password(password):
#         access_token = create_access_token(identity=user.id)
#         return jsonify({"message": "Login successful", "access_token": access_token})
#     else:
#         return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get("email")

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "Email not found"}), 404

    # Generate reset token
    reset_token = secrets.token_hex(16)
    user.reset_token = reset_token  # ✅ Save token to user model
    user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
    db.session.commit()

    # Send email with reset token (not just the link)
    try:
        msg = Message("Password Reset Request",
                      sender=current_app.config["MAIL_USERNAME"],
                      recipients=[email])
        msg.body = f"""
        Here is your password reset token:
        {reset_token}

        Copy this token and use it on the reset password page.
        If you did not request this, ignore this email.
        """
        mail.send(msg)  # ✅ Send email
        return jsonify({"message": "Password reset email sent"}), 200
    except Exception as e:
        return jsonify({"error": f"Email sending failed: {str(e)}"}), 500

@auth_bp.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    reset_token = data.get("reset_token")
    new_password = data.get("password")

    if not reset_token or not new_password:
        return jsonify({"error": "Reset token and new password are required"}), 400

    user = User.query.filter_by(reset_token=reset_token).first()

    if not user or user.reset_token_expiry < datetime.utcnow():
        return jsonify({"error": "Invalid or expired token"}), 400

    # Update password
    user.password_hash = generate_password_hash(new_password)
    user.reset_token = None  # ✅ Clear token after use
    user.reset_token_expiry = None
    db.session.commit()

    return jsonify({"message": "Password reset successful"}), 200

# @auth_bp.route('/admin_login', methods=['POST'])
# def admin_login():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')

#     user = User.query.filter_by(username=username).first()

#     if user and user.check_password(password):
#         if user.is_admin:  # ✅ Check if the user is an admin
#             access_token = create_access_token(identity=user.id)
#             return jsonify({"message": "Admin login successful", "access_token": access_token, "redirect_url": "/pages/admin_dashboard.py"}), 200
#         else:
#             return jsonify({"error": "Access Denied: You are not an admin"}), 403
#     else:
#         return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route('/admin_login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        if user.is_admin:
            access_token = create_access_token(identity=str(user.id))  # Convert to string
            return jsonify({"message": "Admin login successful", "access_token": access_token, "redirect_url": "/pages/admin_dashboard.py"}), 200
        else:
            return jsonify({"error": "Access Denied: You are not an admin"}), 403
    else:
        return jsonify({"error": "Invalid credentials"}), 401