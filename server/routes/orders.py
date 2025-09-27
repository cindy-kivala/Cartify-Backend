# server/routes/orders.py
from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import Order, OrderItem, User, Product

orders_bp = Blueprint("orders_bp", __name__)

# Get user orders
@orders_bp.route("/<username>", methods=["GET"], strict_slashes=False)
def get_orders(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify([]), 404
    orders = Order.query.filter_by(user_id=user.id).all()
    return jsonify([o.to_dict() for o in orders])


# Create order
@orders_bp.route("/", methods=["POST"], strict_slashes=False)
def create_order():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    order = Order(user_id=user.id)
    db.session.add(order)
    db.session.commit()

    # Add order items
    for item_data in data.get("items", []):
        product = Product.query.get(item_data["product_id"])
        if product:
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item_data.get("quantity", 1)
            )
            db.session.add(order_item)
    db.session.commit()

    return jsonify(order.to_dict()), 201


# Delete order
@orders_bp.route("/<int:order_id>", methods=["DELETE"], strict_slashes=False)
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted"})
