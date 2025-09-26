# server/routes/products.py
from flask import Blueprint, jsonify, request
from ..app import db
from ..models import Product

products_bp = Blueprint("products", __name__)

@products_bp.route("/", methods=["GET"])
def get_products():
    return jsonify([p.to_dict() for p in Product.query.all()])

@products_bp.route("/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict())

@products_bp.route("/", methods=["POST"])
def create_product():
    data = request.json
    product = Product(
        name=data["name"],
        price=data["price"],
        description=data.get("description", ""),
        image_url=data.get("image_url", ""),
        category=data.get("category", ""),
        brand=data.get("brand", ""),
        stock=data.get("stock", 0)
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201
