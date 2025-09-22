from flask import Blueprint, request, jsonify
from server import db
from server.models import Order, Product, User

orders_bp = Blueprint("orders", __name__)