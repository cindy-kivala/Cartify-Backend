from flask import Blueprint, request, jsonify
from .models import db, User, Product, CartItem

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")


#Test route
@cart_bp.route("/test")
def test_cart():
    return jsonify({"message": "Cart route is working!"})


#GET cart items 
@cart_bp.route("/<int:user_id>", methods=["GET"])
def get_cart(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    cart_items = CartItem.query.filter_by(user_id=user.id).all()
    if not cart_items:
        return jsonify({"message": "Cart is empty", "items": []}), 200

    return jsonify([item.to_dict() for item in cart_items]), 200


# POST add item to cart 
@cart_bp.route("", methods=["POST"])
def add_to_cart():
    data = request.get_json(force=True)

    user_id = data.get("user_id")
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if not user_id or not product_id:
        return jsonify({"error": "Missing user_id or product_id"}), 400

    user = User.query.get(user_id)
    product = Product.query.get(product_id)

    if not user:
        return jsonify({"error": "User not found"}), 404
    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Check if the product is already in the cart
    existing_item = CartItem.query.filter_by(
        user_id=user.id, product_id=product.id
    ).first()

    if existing_item:
        existing_item.quantity += quanti_
