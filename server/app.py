# server/app.py
from flask import Flask, jsonify
from flask_cors import CORS
from .extensions import db, migrate, bcrypt
from .models import User, Product, Order
from .routes import auth_bp, cart_bp, products_bp, orders_bp, users_bp
import os

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

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

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Enable CORS
    CORS(
        app,
        origins=[
            "https://cartify-dept.netlify.app",
            "http://localhost:5173"
        ],
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
        expose_headers=["Authorization"],
        methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"]
    )

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(cart_bp, url_prefix="/cart")
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(orders_bp, url_prefix="/orders")
    app.register_blueprint(users_bp, url_prefix="/users")

    # Root endpoint
    @app.route("/")
    def index():
        return jsonify({"message": "Cartify Backend is live!"})

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=False)
