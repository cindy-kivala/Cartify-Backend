# server/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from .models import db, bcrypt, User, Product, Order
from flask_migrate import Migrate
from server.auth import auth_bp
from server.cart import cart_bp
import os

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # -------------------- Database --------------------
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev_fallback_key")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'store.db')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    CORS(app,
      origins=["https://cartify-dept.netlify.app"],
      supports_credentials=True,
      allow_headers="*",
      methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"]
    )

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(cart_bp)  

    #  Root 
    @app.route("/")
    def index():
        return jsonify({"message": "Cartify Backend is live!"})

    #  Products
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

        # Orders
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
        user = User.query.filter_by(username=data["username"]).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        order = Order(user_id=user.id, total=data["total"])
        db.session.add(order)
        db.session.commit()
        return jsonify(order.to_dict()), 201

    @app.route("/orders/<int:order_id>", methods=["DELETE"])
    def delete_order(order_id):
        order = Order.query.get(order_id)
        if not order:
            return jsonify({"error": "Order not found"}), 404
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order deleted"})


    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=False)
