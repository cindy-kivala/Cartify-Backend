# server/app.py
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from server.models import db, Product, User, CartItem, Order, OrderItem

# For demonstration, assume Alice is the logged-in user
CURRENT_USER = "Alice"

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Migrate(app, db)

    # --------------------
    # Product Routes
    # --------------------
    @app.route("/products", methods=["GET"])
    def get_products():
        products = Product.query.all()
        return jsonify([p.to_dict() for p in products])

    @app.route("/products/<int:id>", methods=["GET"])
    def get_product(id):
        product = Product.query.get_or_404(id)
        return jsonify(product.to_dict())

    @app.route("/products", methods=["POST"])
    def create_product():
        data = request.json
        try:
            new_product = Product(name=data["name"], price=data["price"])
            db.session.add(new_product)
            db.session.commit()
            return jsonify(new_product.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    @app.route("/products/<int:id>", methods=["PATCH"])
    def update_product(id):
        product = Product.query.get_or_404(id)
        data = request.json
        if "name" in data:
            product.name = data["name"]
        if "price" in data:
            product.price = data["price"]
        db.session.commit()
        return jsonify(product.to_dict())

    @app.route("/products/<int:id>", methods=["DELETE"])
    def delete_product(id):
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted"}), 200

    # --------------------
    # Cart Routes
    # --------------------
    @app.route("/cart", methods=["GET"])
    def get_cart():
        user = User.query.filter_by(username=CURRENT_USER).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        cart_items = CartItem.query.filter_by(user_id=user.id).all()
        return jsonify([item.to_dict() for item in cart_items])

    @app.route("/cart", methods=["POST"])
    def add_to_cart():
        data = request.json
        product_id = data.get("product_id")
        quantity = data.get("quantity", 1)

        user = User.query.filter_by(username=CURRENT_USER).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        # Check if item already in cart
        existing_item = CartItem.query.filter_by(user_id=user.id, product_id=product.id).first()
        if existing_item:
            existing_item.quantity += quantity
            db.session.commit()
            return jsonify(existing_item.to_dict()), 200

        cart_item = CartItem(user_id=user.id, product_id=product.id, quantity=quantity)
        db.session.add(cart_item)
        db.session.commit()

        return jsonify(cart_item.to_dict()), 201

    @app.route("/cart/<int:id>", methods=["PATCH"])
    def update_cart_item(id):
        data = request.json
        quantity = data.get("quantity", 1)
        cart_item = CartItem.query.get_or_404(id)
        cart_item.quantity = quantity
        db.session.commit()
        return jsonify(cart_item.to_dict())

    @app.route("/cart/<int:id>", methods=["DELETE"])
    def remove_cart_item(id):
        cart_item = CartItem.query.get_or_404(id)
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({"message": "Cart item removed"}), 200

    # --------------------
    # Order Routes
    # --------------------
    @app.route("/orders", methods=["POST"])
    def create_order():
        user = User.query.filter_by(username=CURRENT_USER).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Get all cart items for current user
        cart_items = CartItem.query.filter_by(user_id=user.id).all()
        if not cart_items:
            return jsonify({"error": "Cart is empty"}), 400

        order = Order(user_id=user.id)
        db.session.add(order)
        db.session.flush()

        for item in cart_items:
            order_item = OrderItem(order_id=order.id, product_id=item.product_id, quantity=item.quantity)
            db.session.add(order_item)
            db.session.delete(item)  # Clear cart

        db.session.commit()
        return jsonify(order.to_dict()), 201

    @app.route("/orders", methods=["GET"])
    def get_orders():
        user = User.query.filter_by(username=CURRENT_USER).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        orders = Order.query.filter_by(user_id=user.id).all()
        return jsonify([order.to_dict() for order in orders])

    return app


# --------------------
# Run server
# --------------------
if __name__ == "__main__":
    app = create_app()
    app.run(port=5000, debug=True)
