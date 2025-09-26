# server/cart.py
from flask import Blueprint, request, jsonify
from .models import db, User, Product, CartItem, Order, OrderItem

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")

# ---------------- GET CART ITEMS ----------------
@cart_bp.route("/<username>", methods=["GET"])
def get_cart(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    cart_items = CartItem.query.filter_by(user_id=user.id).all()
    result = []
    total_quantity = 0
    total_price = 0.0

    for item in cart_items:
        product = item.product
        if not product:
            continue  # skip deleted products

        total_quantity += item.quantity
        total_price += product.price * item.quantity
        result.append(item.to_dict())

    return jsonify({
        "items": result,
        "total": total_quantity,
        "total_price": total_price
    }), 200


# ---------------- ADD ITEM TO CART ----------------
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

    existing_item = CartItem.query.filter_by(user_id=user.id, product_id=product.id).first()
    if existing_item:
        new_quantity = existing_item.quantity + quantity
        if new_quantity > product.stock:
            return jsonify({"error": f"Only {product.stock} items available"}), 400
        existing_item.quantity = new_quantity
    else:
        if quantity > product.stock:
            return jsonify({"error": f"Only {product.stock} items available"}), 400
        new_item = CartItem(user_id=user.id, product_id=product.id, quantity=quantity)
        db.session.add(new_item)

    db.session.commit()
    return jsonify({"message": "Item added to cart"}), 201


# ---------------- UPDATE CART ITEM QUANTITY ----------------
@cart_bp.route("/item/<int:item_id>", methods=["PATCH"])
def update_cart_item(item_id):
    data = request.get_json(force=True)
    quantity = data.get("quantity")

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid quantity"}), 400

    if quantity < 1:
        return jsonify({"error": "Quantity must be at least 1"}), 400

    item = CartItem.query.get(item_id)
    if not item:
        return jsonify({"error": "Cart item not found"}), 404

    product = item.product
    if not product:
        return jsonify({"error": "Product not found"}), 404

    if quantity > product.stock:
        return jsonify({"error": f"Only {product.stock} items available"}), 400

    item.quantity = quantity
    db.session.commit()

    return jsonify(item.to_dict()), 200


# ---------------- REMOVE CART ITEM ----------------
@cart_bp.route("/item/<int:item_id>", methods=["DELETE"])
def remove_cart_item(item_id):
    item = CartItem.query.get(item_id)
    if not item:
        return jsonify({"error": "Cart item not found"}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item removed"}), 200


# ---------------- CHECKOUT ----------------
@cart_bp.route("/checkout/<username>", methods=["POST"])
def checkout_cart(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    cart_items = CartItem.query.filter_by(user_id=user.id).all()
    if not cart_items:
        return jsonify({"error": "Cart is empty"}), 400

    order = Order(user_id=user.id)
    db.session.add(order)
    db.session.flush()  # to get order.id

    for item in cart_items:
        product = item.product
        if not product:
            return jsonify({"error": f"Product with id {item.product_id} not found"}), 404

        if item.quantity > product.stock:
            return jsonify({"error": f"Not enough stock for {product.name}"}), 400

        product.stock -= item.quantity
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price
        )
        db.session.add(order_item)
        db.session.delete(item)

    db.session.commit()
    return jsonify({"message": "Checkout successful!", "order_id": order.id}), 200
