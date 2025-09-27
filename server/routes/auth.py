# server/routes/auth.py
from flask import Blueprint, request, jsonify
from server.models import User
from ..extensions import db

auth_bp = Blueprint("auth", __name__)

#  REGISTER 
@auth_bp.route("/register", methods=["POST"], strict_slashes=False)
def register():
    data = request.get_json()

    if not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "All fields are required"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400

    new_user = User(username=data["username"], email=data["email"])
    new_user.password = data["password"]  # bcrypt auto-hash via model setter

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201


# LOGIN 
@auth_bp.route("/login", methods=["POST"], strict_slashes=False)
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get("email")).first()

    if not user or not user.check_password(data.get("password")):
        return jsonify({"error": "Invalid credentials"}), 401

    # Stateless → frontend decides how to "store" login
    return jsonify({
        "message": "Login successful",
        "user": user.to_dict()
    }), 200


# LOGOUT
@auth_bp.route("/logout", methods=["POST"], strict_slashes=False)
def logout():
    # Stateless → just return a message
    return jsonify({"message": "Logout successful"}), 200
