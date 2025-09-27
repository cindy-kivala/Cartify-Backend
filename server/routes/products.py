# server/routes/products.py
from flask import Blueprint, jsonify, request
from ..extensions import db
from ..models import Product

products_bp = Blueprint("products_bp", __name__)

# Get all products
@products_bp.route("/", methods=["GET"], strict_slashes=False)
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])


# Get single product by ID
@products_bp.route("/<int:id>", methods=["GET"], strict_slashes=False)
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict())


# Create product
@products_bp.route("/", methods=["POST"], strict_slashes=False)
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
