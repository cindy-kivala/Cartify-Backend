from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import CartItem, Product, User

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")

# Get user's cart by user_id
@cart_bp.route("/user/<int:user_id>", methods=["GET"])
def get_cart(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    items = CartItem.query.filter_by(user_id=user.id).all()
    cart_data = []
    total_quantity = 0
    total_price = 0.0
    
    for item in items:
        if item.product:  # Make sure product exists
            item_dict = item.to_dict()
            cart_data.append(item_dict)
            total_quantity += item.quantity
            total_price += item.product.price * item.quantity
    
    return jsonify({
        "items": cart_data,
        "total_quantity": total_quantity,
        "total_price": total_price
    })

# Add to cart - FIXED
@cart_bp.route("/", methods=["POST"])
def add_to_cart():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        print(f"Received data: {data}")  # Debug log
        
        user_id = data.get("user_id")
        product_id = data.get("product_id")
        quantity = data.get("quantity", 1)

        # Debug: check what we received
        print(f"user_id: {user_id}, product_id: {product_id}, quantity: {quantity}")

        if not user_id or not product_id:
            return jsonify({"error": "Missing user_id or product_id"}), 400

        user = User.query.get(user_id)
        product = Product.query.get(product_id)

        if not user:
            return jsonify({"error": "User not found"}), 404
        if not product:
            return jsonify({"error": "Product not found"}), 404

        # Check stock
        if product.stock < quantity:
            return jsonify({"error": f"Only {product.stock} items available"}), 400

        # Check if item already in cart
        existing_item = CartItem.query.filter_by(user_id=user.id, product_id=product.id).first()
        
        if existing_item:
            new_quantity = existing_item.quantity + quantity
            if new_quantity > product.stock:
                return jsonify({"error": f"Only {product.stock} items available"}), 400
            existing_item.quantity = new_quantity
            cart_item = existing_item
        else:
            cart_item = CartItem(user_id=user.id, product_id=product.id, quantity=quantity)
            db.session.add(cart_item)

        db.session.commit()
        return jsonify({"message": "Item added to cart", "item": cart_item.to_dict()}), 201

    except Exception as e:
        print(f"Error in add_to_cart: {str(e)}")  # Debug log
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

# Update cart item quantity 
@cart_bp.route("/item/<int:item_id>", methods=["PATCH"])
def update_cart_item(item_id):
    try:
        data = request.json
        item = CartItem.query.get_or_404(item_id)
        
        quantity = data.get("quantity")
        if not quantity or quantity < 1:
            return jsonify({"error": "Invalid quantity"}), 400
            
        if item.product.stock < quantity:
            return jsonify({"error": f"Only {item.product.stock} items available"}), 400
            
        item.quantity = quantity
        db.session.commit()
        return jsonify(item.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Delete cart item
@cart_bp.route("/item/<int:item_id>", methods=["DELETE"])
def delete_cart_item(item_id):
    try:
        item = CartItem.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item removed from cart"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Checkout
@cart_bp.route("/checkout/<int:user_id>", methods=["POST"])
def checkout(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        cart_items = CartItem.query.filter_by(user_id=user.id).all()
        if not cart_items:
            return jsonify({"error": "Cart is empty"}), 400
            
        # Clear cart after successful checkout
        CartItem.query.filter_by(user_id=user.id).delete()
        db.session.commit()
        
        return jsonify({"message": "Checkout successful"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


