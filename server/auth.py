from flask import Blueprint, request, jsonify
from server.models import db, User

auth_bp = Blueprint("auth", __name__)

# -------------------- SIGNUP --------------------
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    if not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 400
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400

    user = User(username=data["username"], email=data["email"], password=data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

# -------------------- LOGIN --------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get("username")).first()
    if user and user.check_password(data.get("password")):
        return jsonify(user.to_dict())
    return jsonify({"error": "Invalid credentials"}), 401

# -------------------- LOGOUT --------------------
@auth_bp.route("/logout", methods=["POST"])
def logout():
    # For simple API: client deletes token/session
    return jsonify({"message": "Logged out successfully"})
