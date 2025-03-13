from flask import Blueprint, jsonify, request, current_app
from models import db, User, Feedback
from flask_jwt_extended import jwt_required, get_jwt_identity

routes_bp = Blueprint("routes", __name__)

@routes_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "API is running"}), 200

@routes_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
    return jsonify(users_list)

@routes_bp.route('/add_feedback', methods=['POST'])
def add_feedback():
    data = request.get_json()
    if not data or "user_id" not in data or "comments" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        feedback = Feedback(user_id=data["user_id"], comments=data["comments"])
        db.session.add(feedback)
        db.session.commit()
        return jsonify({"message": "Feedback submitted successfully"}), 201
    except Exception as e:
        current_app.logger.error("Error submitting feedback: %s", e)
        return jsonify({"error": "An error occurred while submitting feedback"}), 500

@routes_bp.route('/user_profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "home_address": user.home_address or "",
            "country": user.country or "",
            "region": user.region or "",
            "phone": user.phone or "",
            "profile_pic": user.profile_pic or ""
        }), 200
    except Exception as e:
        current_app.logger.error("Error fetching user profile: %s", e)
        return jsonify({"error": "An error occurred while fetching profile"}), 500

@routes_bp.route('/update_profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Force JSON parsing in case the header is not set correctly
        data = request.get_json(force=True)
        if not data:
            current_app.logger.error("No data provided in update_profile")
            return jsonify({"error": "No data provided"}), 400

        # Debug log for incoming payload
        current_app.logger.info("Updating profile for user %s with data: %s", user_id, data)

        # Update all profile fields from the payload.
        user.email = data.get('email', user.email)
        user.home_address = data.get('home_address', user.home_address)
        user.country = data.get('country', user.country)
        user.region = data.get('region', user.region)
        user.phone = data.get('phone', user.phone)
        user.profile_pic = data.get('profile_pic', user.profile_pic)

        db.session.add(user)
        db.session.flush()
        db.session.commit()
        return jsonify({"message": "Profile updated successfully"}), 200
    except Exception as e:
        current_app.logger.error("Error updating profile: %s", e)
        db.session.rollback()
        return jsonify({"error": "An error occurred while updating profile"}), 500

