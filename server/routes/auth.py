# server/routes/auth.py
from flask import Blueprint, request, jsonify
from server.models import User
from ..extensions import db

# Add URL prefix to match your frontend calls
auth_bp = Blueprint("auth", __name__)

# REGISTER 
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "All fields are required"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400
        
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 400

    new_user = User(username=data["username"], email=data["email"])
    new_user.password = data["password"]  # bcrypt auto-hash via model setter

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201

# SIGNUP endpoint (for your frontend that calls /signup)
@auth_bp.route("/signup", methods=["POST"])
def signup():
    return register()  # Just call the register function

# LOGIN 
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    
    # Support login with either username or email
    username_or_email = data.get("username") or data.get("email")
    password = data.get("password")
    
    if not username_or_email or not password:
        return jsonify({"error": "Username/email and password required"}), 400
    
    # Try to find user by username first, then email
    user = User.query.filter_by(username=username_or_email).first()
    if not user:
        user = User.query.filter_by(email=username_or_email).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify(user.to_dict()), 200

# LOGOUT
@auth_bp.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Logout successful"}), 200