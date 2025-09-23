from flask import Blueprint, request, jsonify
from server import db
from server.models import CartItem, User, Product

cart_bp = Blueprint("cart", __name__)