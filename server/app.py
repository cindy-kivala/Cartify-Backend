# server/app.py
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

from .models import db 

# Initialize extensions
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # -------------------- Config --------------------
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev_fallback_key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'local.db')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # -------------------- Extensions --------------------
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, supports_credentials=True, expose_headers=["Content-Type", "Authorization"])

    # -------------------- Blueprints --------------------
    from .routes import auth_bp, products_bp, cart_bp, orders_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(cart_bp, url_prefix="/cart")
    app.register_blueprint(orders_bp, url_prefix="/orders")

    # Root endpoint
    @app.route("/")
    def index():
        return jsonify({"message": "Cartify Backend is live!"})

    return app

# Optional local run
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
