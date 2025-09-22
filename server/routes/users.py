from flask import Blueprint, request, jsonify
from server import db
from server.models import User

users_bp = Blueprint("users", __name__)