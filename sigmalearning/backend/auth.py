from flask import Blueprint, request, jsonify, url_for, current_app, Response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User
from werkzeug.security import generate_password_hash
import secrets
from flask_mail import Message
from config import mail
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from twilio.rest import Client
import os

auth_bp = Blueprint("auth", __name__)

def get_serializer():
    # Create the serializer within an application context
    return URLSafeTimedSerializer(current_app.config["JWT_SECRET_KEY"])

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not all(k in data for k in ["username", "email", "password"]):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400

    try:
        # Instead of saving the user immediately, create a dictionary of user data.
        user_data = {
            "username": data["username"],
            "email": data["email"],
            "password_hash": generate_password_hash(data["password"])
        }
        # Create a signed token that holds the new user data.
        serializer = get_serializer()
        token = serializer.dumps(user_data)
        
        # Send verification email
        try:
            msg = Message("Verify Your Email",
                          sender=current_app.config["MAIL_DEFAULT_SENDER"],
                          recipients=[data['email']])
            # Generate a fully qualified URL for email verification with the token.
            verify_link = url_for('auth.verify_email', token=token, _external=True)
            msg.body = f"Thank you for registering. Please verify your email by clicking the following link:\n{verify_link}"
            mail.send(msg)
        except Exception as e:
            current_app.logger.error("Verification email sending failed: %s", e)
        
        # Inform the user to check their email.
        return jsonify({"message": "User registered successfully. Please check your email to verify your account."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/verify_email', methods=['GET'], endpoint="verify_email")
def verify_email():
    token = request.args.get("token")
    if not token:
        return jsonify({"error": "Missing token"}), 400

    serializer = get_serializer()
    try:
        # The token is valid for 1 hour (3600 seconds)
        user_data = serializer.loads(token, max_age=3600)
    except SignatureExpired:
        return jsonify({"error": "Token expired"}), 400
    except BadSignature:
        return jsonify({"error": "Invalid token"}), 400

    # Check if the user already exists to avoid duplicates.
    if User.query.filter_by(username=user_data["username"]).first():
        return jsonify({"error": "User already verified"}), 400

    try:
        # Now create and save the user record as the email is verified.
        user = User(username=user_data["username"], email=user_data["email"])
        user.password_hash = user_data["password_hash"]
        user.email_verified = True
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    html_content = """
    <html>
    <head>
        <meta http-equiv="refresh" content="3; url=http://127.0.0.1:8501/pages/learners_dashboard.py">
        <title>Email Verified</title>
    </head>
    <body>
        <p>Your email has been verified successfully. Redirecting to your dashboard...</p>
        <script>
            window.location.href = "http://127.0.0.1:8501/pages/learners_dashboard.py";
        </script>
    </body>
    </html>
    """
    return Response(html_content, mimetype='text/html')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        if not user.email_verified:
            return jsonify({"error": "Email not verified. Please verify your email before logging in."}), 403
        # If 2FA is enabled, send a login 2FA code and do not issue the access token immediately.
        if user.two_fa_enabled:
            login_code = f"{secrets.randbelow(1000000):06}"
            user.login_2fa_code = login_code
            user.login_2fa_expiry = datetime.utcnow() + timedelta(minutes=5)
            db.session.commit()
            current_app.logger.info("2FA login code for user %s: %s", user.username, login_code)
            return jsonify({"message": "2FA code sent to your phone. Please verify.", "two_fa_required": True}), 200
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"message": "Login successful", "access_token": access_token})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route('/verify_login_2fa', methods=['POST'])
def verify_login_2fa():
    data = request.get_json()
    username = data.get('username')
    code = data.get('code')
    if not username or not code:
        return jsonify({"error": "Username and 2FA code are required"}), 400
    user = User.query.filter_by(username=username).first()
    if not user or not user.two_fa_enabled:
        return jsonify({"error": "2FA not activated for this user"}), 400
    if user.login_2fa_code != code or (user.login_2fa_expiry is not None and user.login_2fa_expiry < datetime.utcnow()):
        return jsonify({"error": "Invalid or expired 2FA code"}), 400
    user.login_2fa_code = None
    user.login_2fa_expiry = None
    db.session.commit()
    access_token = create_access_token(identity=str(user.id))
    return jsonify({"message": "Login successful", "access_token": access_token})

@auth_bp.route('/activate_2fa', methods=['POST'])
@jwt_required()
def activate_2fa():
    data = request.get_json()
    phone = data.get("phone")
    if not phone:
        return jsonify({"error": "Phone number is required"}), 400
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user.phone = phone
    activation_code = f"{secrets.randbelow(1000000):06}"
    user.activation_2fa_code = activation_code
    user.activation_2fa_expiry = datetime.utcnow() + timedelta(minutes=5)
    db.session.commit()

    try:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_phone = os.getenv("TWILIO_FROM_PHONE")
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"Your 2FA activation code is: {activation_code}",
            from_=from_phone,
            to=phone
        )
    except Exception as e:
        current_app.logger.error("Failed to send SMS: %s", e)
        return jsonify({"error": "Failed to send activation code via SMS"}), 500

    return jsonify({"message": "Activation code sent to your phone"}), 200

@auth_bp.route('/verify_2fa_activation', methods=['POST'])
@jwt_required()
def verify_2fa_activation():
    data = request.get_json()
    code = data.get("activation_code")
    if not code:
        return jsonify({"error": "Activation code is required"}), 400
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    if user.activation_2fa_code != code or (user.activation_2fa_expiry is not None and user.activation_2fa_expiry < datetime.utcnow()):
        return jsonify({"error": "Invalid or expired activation code"}), 400
    user.two_fa_enabled = True
    user.activation_2fa_code = None
    user.activation_2fa_expiry = None
    db.session.commit()
    return jsonify({"message": "2FA activated successfully"}), 200

@auth_bp.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get("email")
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "Email not found"}), 404

    reset_token = secrets.token_hex(16)
    user.reset_token = reset_token
    user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
    db.session.commit()

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
        mail.send(msg)
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
    if not user or (user.reset_token_expiry is not None and user.reset_token_expiry < datetime.utcnow()):
        return jsonify({"error": "Invalid or expired token"}), 400
    user.password_hash = generate_password_hash(new_password)
    user.reset_token = None
    user.reset_token_expiry = None
    db.session.commit()
    return jsonify({"message": "Password reset successful"}), 200

@auth_bp.route('/update_2fa_setting', methods=['POST'])
@jwt_required()
def update_2fa_setting():
    data = request.get_json()
    password = data.get("password")
    new_setting = data.get("two_fa_enabled")
    if password is None or new_setting is None:
        return jsonify({"error": "Password and new setting are required"}), 400
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid password"}), 403
    user.two_fa_enabled = new_setting
    db.session.commit()
    return jsonify({"message": "2FA setting updated successfully"}), 200

@auth_bp.route('/admin_login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        if user.is_admin:
            access_token = create_access_token(identity=str(user.id))
            return jsonify({"message": "Admin login successful", "access_token": access_token, "redirect_url": "/pages/admin_dashboard.py"}), 200
        else:
            return jsonify({"error": "Access Denied: You are not an admin"}), 403
    else:
        return jsonify({"error": "Invalid credentials"}), 401
