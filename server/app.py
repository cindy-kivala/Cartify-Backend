
# server/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from .models import db, User, Product, Order
from flask_migrate import Migrate
from .routes import auth_bp, cart_bp, products_bp, orders_bp
import os

migrate = Migrate()

def create_app():
    app = Flask(__name__)

     # -------------------- Configuration --------------------
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev_fallback_key")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Use PostgreSQL in production if DATABASE_URL is set
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        # Render uses "postgres://", which SQLAlchemy needs as "postgresql://"
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url.replace(
            "postgres://", "postgresql://", 1
        )
    else:
        # Local development uses SQLite
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'local.db')}"

    db.init_app(app)
    migrate.init_app(app, db)

    CORS(app,
        origins=[
            "https://cartify-dept.netlify.app",
            "http://localhost:5173"
        ],
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
        expose_headers=["Authorization"],
        methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"]
    )

    # Register all blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)

    # Root endpoint
    @app.route("/")
    def index():
        return jsonify({"message": "Cartify Backend is live!"})

    # Seed data endpoint for testing
    @app.route("/seed", methods=["POST"])
    def seed_database():
        if Product.query.count() == 0:
            sample_products = [
                Product(
                    name="Wireless Headphones",
                    price=199.99,
                    description="High-quality wireless headphones with noise cancellation",
                    image_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500",
                    category="Electronics",
                    brand="TechBrand",
                    stock=50
                ),
                Product(
                    name="Smartphone",
                    price=699.99,
                    description="Latest model smartphone with advanced features",
                    image_url="https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500",
                    category="Electronics",
                    brand="PhoneCorp",
                    stock=30
                ),
                Product(
                    name="Laptop",
                    price=1299.99,
                    description="High-performance laptop for work and gaming",
                    image_url="https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500",
                    category="Computers",
                    brand="CompTech",
                    stock=20
                ),
                Product(
                    name="Coffee Maker",
                    price=89.99,
                    description="Programmable coffee maker with thermal carafe",
                    image_url="https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=500",
                    category="Home & Kitchen",
                    brand="BrewMaster",
                    stock=25
                ),
                Product(
                    name="Gaming Chair",
                    price=299.99,
                    description="Ergonomic gaming chair with lumbar support",
                    image_url="https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=500",
                    category="Furniture",
                    brand="GameComfort",
                    stock=15
                )
            ]
            for product in sample_products:
                db.session.add(product)
            db.session.commit()
            return jsonify({"message": "Database seeded with sample products"}), 201
        return jsonify({"message": "Database already has products"}), 200

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=False)