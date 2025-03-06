from flask import Blueprint, jsonify, request
from models import db, User, Feedback

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
        return jsonify({"error": str(e)}), 500
