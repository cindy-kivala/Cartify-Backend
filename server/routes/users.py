# server/routes/users.py
from flask import Blueprint, request, jsonify
from server.models import User
from ..extensions import db

users_bp = Blueprint("users_bp", __name__)

#  Get all users 
@users_bp.route("/", methods=["GET"], strict_slashes=False)
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

#  Get single user 
@users_bp.route("/<int:user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200

# Update user
@users_bp.route("/<int:user_id>", methods=["PATCH"], strict_slashes=False)
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if "username" in data:
        user.username = data["username"]
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.password = data["password"]  # auto-hash

    db.session.commit()
    return jsonify(user.to_dict()), 200

#  Delete user 
@users_bp.route("/<int:user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200
