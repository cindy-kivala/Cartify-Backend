from flask import Blueprint, request, jsonify
from server import db
from server.models import Product

products_bp = Blueprint("products", __name__)