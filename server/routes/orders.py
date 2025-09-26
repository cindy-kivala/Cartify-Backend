# server/routes/orders.py
from flask import Blueprint, request, jsonify
from ..app import db
from ..models import Order, User

orders_bp = Blueprint("orders_bp", __name__)

@orders_bp.route("/<username>", methods=["GET"])
def get_orders(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify([]), 404
    orders = Order.query.filter_by(user_id=user.id).all()
    return jsonify([o.to_dict() for o in orders])

@orders_bp.route("/", methods=["POST"])
def create_order():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    order = Order(user_id=user.id, total=data["total"])
    db.session.add(order)
    db.session.commit()
    return jsonify(order.to_dict()), 201

@orders_bp.route("/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted"})
