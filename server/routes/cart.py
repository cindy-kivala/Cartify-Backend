#server/routes/cart.py
from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import CartItem, Product, User

cart_bp = Blueprint("cart_bp", __name__)

# Get user's cart
@cart_bp.route("/<username>", methods=["GET"], strict_slashes=False)
def get_cart(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify([]), 404
    items = CartItem.query.filter_by(user_id=user.id).all()
    return jsonify([i.to_dict() for i in items])


# Add to cart
@cart_bp.route("/", methods=["POST"], strict_slashes=False)
def add_to_cart():
    data = request.get_json()  # safer than request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    username = data.get("username")
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if not username or not product_id:
        return jsonify({"error": "Missing username or product_id"}), 400

    user = User.query.filter_by(username=username).first()
    product = Product.query.get(product_id)

    if not user:
        return jsonify({"error": "User not found"}), 404
    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Check if item already in cart
    cart_item = CartItem.query.filter_by(user_id=user.id, product_id=product.id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=user.id, product_id=product.id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    return jsonify(cart_item.to_dict()), 201


# Update cart item quantity
@cart_bp.route("/item/<int:item_id>", methods=["PATCH"], strict_slashes=False)
def update_cart_item(item_id):
    data = request.json
    item = CartItem.query.get_or_404(item_id)
    item.quantity = data["quantity"]
    db.session.commit()
    return jsonify(item.to_dict())


# Delete cart item
@cart_bp.route("/item/<int:item_id>", methods=["DELETE"], strict_slashes=False)
def delete_cart_item(item_id):
    item = CartItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item removed from cart"})


# Checkout
@cart_bp.route("/checkout/<username>", methods=["POST"], strict_slashes=False)
def checkout(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    CartItem.query.filter_by(user_id=user.id).delete()
    db.session.commit()
    return jsonify({"message": "Checkout successful"})
