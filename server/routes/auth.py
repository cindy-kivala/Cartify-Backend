# server/routes/auth.py
from flask import Blueprint, request, jsonify, session
from ..app import db
from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 400

    user = User(
        username=data["username"],
        password_hash=generate_password_hash(data["password"])
    )
    db.session.add(user)
    db.session.commit()
    session["username"] = user.username
    return jsonify({"message": "User created", "username": user.username}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    if not user or not check_password_hash(user.password_hash, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    session["username"] = user.username
    return jsonify({"message": "Logged in", "username": user.username})

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    return jsonify({"message": "Logged out"})
