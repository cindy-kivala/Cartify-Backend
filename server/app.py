# server/app.py
from flask import Flask, request, jsonify
from server import db, migrate  # db and migrate are defined in server/__init__.py
from server.models import Product, Order, User, CartItem, OrderItem  # import models so they're registered

def create_app():
    app = Flask(__name__)
    # Use an absolute path or environment-configured DB in prod; this is fine for local dev
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # ---------- Product routes ----------
    @app.route("/products", methods=["GET"])
    def get_products():
        products = Product.query.all()
        return jsonify([{"id": p.id, "name": p.name, "price": p.price} for p in products])

    @app.route("/products/<int:id>", methods=["GET"])
    def get_product(id):
        product = Product.query.get_or_404(id)
        return jsonify({"id": product.id, "name": product.name, "price": product.price})

    @app.route("/products", methods=["POST"])
    def create_product():
        data = request.json or {}
        try:
            new_product = Product(name=data["name"], price=data["price"])
            db.session.add(new_product)
            db.session.commit()
            return jsonify({"id": new_product.id, "name": new_product.name, "price": new_product.price}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    @app.route("/products/<int:id>", methods=["PATCH"])
    def update_product(id):
        product = Product.query.get_or_404(id)
        data = request.json or {}
        if "name" in data:
            product.name = data["name"]
        if "price" in data:
            product.price = data["price"]
        db.session.commit()
        return jsonify({"id": product.id, "name": product.name, "price": product.price})

    @app.route("/products/<int:id>", methods=["DELETE"])
    def delete_product(id):
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted"}), 200

    # ---------- Orders routes ----------
    # create order (simple endpoint — matches the structure used earlier)
    @app.route("/orders", methods=["POST"])
    def create_order():
        data = request.json or {}
        try:
            order = Order(
                user_name=data.get("user_name"),
                product_id=data.get("product_id"),
                quantity=data.get("quantity", 1)
            )
            db.session.add(order)
            db.session.commit()
            return jsonify({
                "id": order.id,
                "user_name": order.user_name,
                "product_id": order.product_id,
                "quantity": order.quantity
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    @app.route("/orders/<string:username>", methods=["GET"])
    def get_orders(username):
        orders = Order.query.filter_by(user_name=username).all()
        return jsonify([
            {
                "id": o.id,
                "user_name": o.user_name,
                "product": getattr(o, "product", None).name if getattr(o, "product", None) else None,
                "quantity": o.quantity,
                "price": getattr(o, "product", None).price if getattr(o, "product", None) else None
            }
            for o in orders
        ])

    return app


# Export an app instance for Flask CLI convenience (so `flask --app server.app` works)
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
