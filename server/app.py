from flask import Flask
from flask_cors import CORS
from server import db, migrate
from server.config import Config


def create_app():
    app = Flask(__name__)

   
    app.config.from_object(Config)

#binding the db and migrate to the app
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    from server.models import Product, User, Order, CartItem, OrderItem

#Register blueprints
    from server.routes.users import users_bp
    from server.routes.cart import cart_bp
    from server.routes.products import products_bp
    from server.routes.orders import orders_bp

    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(cart_bp, url_prefix="/cart")
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(orders_bp, url_prefix="/orders")

    return app