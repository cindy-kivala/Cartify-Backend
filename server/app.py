# server/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from .models import db, bcrypt, User, Product, CartItem, Order, OrderItem
from flask_migrate import Migrate
from server.auth import auth_bp
import os

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # -------------------- Database --------------------
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'store.db')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # -------------------- Blueprints --------------------
    app.register_blueprint(auth_bp)

    # -------------------- Products --------------------
    @app.route("/products", methods=["GET"])
    def get_products():
        return jsonify([p.to_dict() for p in Product.query.all()])

    @app.route("/products/<int:id>", methods=["GET"])
    def get_product(id):
        product = Product.query.get_or_404(id)
        return jsonify(product.to_dict())

    @app.route("/products", methods=["POST"])
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

    # -------------------- Cart --------------------
    @app.route("/cart/<string:username>", methods=["GET"])
    def get_cart(username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify([]), 404
        cart_items = CartItem.query.filter_by(user_id=user.id).all()
        return jsonify([item.to_dict() for item in cart_items])

    @app.route("/cart", methods=["POST"])
    def add_to_cart():
        data = request.json
        user = User.query.filter_by(username=data["username"]).first()
        product = Product.query.get(data["product_id"])
        if not user or not product:
            return jsonify({"error": "Invalid user or product"}), 400

        if product.stock <= 0:
            return jsonify({"error": "Product is out of stock"}), 400

        existing_item = CartItem.query.filter_by(user_id=user.id, product_id=product.id).first()
        if existing_item:
            new_quantity = existing_item.quantity + data.get("quantity", 1)
            if new_quantity > product.stock:
                return jsonify({"error": f"Only {product.stock} items available"}), 400
            existing_item.quantity = new_quantity
            db.session.commit()
            return jsonify(existing_item.to_dict()), 200

        item = CartItem(
            user_id=user.id,
            product_id=product.id,
            quantity=data.get("quantity", 1)
        )
        db.session.add(item)
        db.session.commit()
        return jsonify(item.to_dict()), 201

    @app.route("/cart/<int:item_id>", methods=["DELETE"])
    def remove_from_cart(item_id):
        item = CartItem.query.get(item_id)
        if not item:
            return jsonify({"error": "Cart item not found"}), 404
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item removed from cart"}), 200

    @app.route("/cart/<int:item_id>", methods=["PATCH"])
    def update_cart_item(item_id):
        data = request.json
        cart_item = CartItem.query.get(item_id)
        if not cart_item:
            return jsonify({"error": "Cart item not found"}), 404

        if "quantity" in data:
            try:
                new_quantity = int(data["quantity"])
                if new_quantity <= 0:
                    return jsonify({"error": "Quantity must be greater than 0"}), 400
                if new_quantity > cart_item.product.stock:
                    return jsonify({"error": f"Only {cart_item.product.stock} items available"}), 400
                cart_item.quantity = new_quantity
            except ValueError:
                return jsonify({"error": "Invalid quantity"}), 400

        db.session.commit()
        return jsonify(cart_item.to_dict()), 200

    # -------------------- Checkout --------------------
    @app.route("/checkout/<string:username>", methods=["POST"])
    def checkout(username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        cart_items = CartItem.query.filter_by(user_id=user.id).all()
        if not cart_items:
            return jsonify({"error": "Cart is empty"}), 400

        order = Order(user_id=user.id)
        db.session.add(order)
        db.session.flush()  # get order.id without committing

        for item in cart_items:
            product = Product.query.get(item.product_id)
            if not product:
                return jsonify({"error": f"Product with id {item.product_id} not found"}), 404

            # Check stock
            if item.quantity > product.stock:
                return jsonify({"error": f"Not enough stock for {product.name}"}), 400

            # Subtract stock
            product.stock -= item.quantity

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item.quantity
            )
            db.session.add(order_item)

            # Remove item from cart
            db.session.delete(item)

        db.session.commit()
        return jsonify(order.to_dict()), 201

    # -------------------- Orders --------------------
    @app.route("/orders/<username>", methods=["GET"])
    def get_orders(username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify([]), 404
        orders = Order.query.filter_by(user_id=user.id).all()
        return jsonify([o.to_dict() for o in orders])

    @app.route("/orders", methods=["POST"])
    def create_order():
        data = request.json
        username = data.get("username")
        items = data.get("items")  # list of {product_id, quantity}

        if not username or not items:
            return jsonify({"error": "Missing data"}), 400

        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        order = Order(user_id=user.id)
        db.session.add(order)
        db.session.flush()  # generate order.id

        for item in items:
            product = Product.query.get(item["product_id"])
            if not product:
                return jsonify({"error": f"Product {item['product_id']} not found"}), 404

            if product.stock < item["quantity"]:
                return jsonify({"error": f"Not enough stock for {product.name}"}), 400

            # Decrease stock
            product.stock -= item["quantity"]

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item["quantity"],
                price=product.price
            )
            db.session.add(order_item)

            # Remove from cart if exists
            cart_item = CartItem.query.filter_by(user_id=user.id, product_id=product.id).first()
            if cart_item:
                db.session.delete(cart_item)

        db.session.commit()
        return jsonify({"message": "Order created successfully", "order_id": order.id})

    @app.route("/orders/<int:order_id>", methods=["DELETE"])
    def delete_order(order_id):
        order = Order.query.get(order_id)
        if not order:
            return jsonify({"error": "Order not found"}), 404
        OrderItem.query.filter_by(order_id=order.id).delete()
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order deleted"}), 200

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
