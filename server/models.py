# server/models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import validates

db = SQLAlchemy()
bcrypt = Bcrypt()


# ---------------- USER ----------------
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column("password_hash", db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    cart_items = db.relationship("CartItem", backref="user", lazy=True)
    orders = db.relationship("Order", backref="user", lazy=True)

    @property
    def password(self):
        raise AttributeError("Password is write-only")

    @password.setter
    def password(self, plaintext):
        self._password_hash = bcrypt.generate_password_hash(plaintext).decode("utf-8")

    def check_password(self, plaintext):
        return bcrypt.check_password_hash(self._password_hash, plaintext)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat()
        }


# ---------------- PRODUCT ----------------
class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=True)
    image_url = db.Column(db.String, nullable=True)
    category = db.Column(db.String, nullable=True)
    brand = db.Column(db.String, nullable=True)
    stock = db.Column(db.Integer, default=0)  # ✅ new field
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    cart_items = db.relationship("CartItem", back_populates="product")
    order_items = db.relationship("OrderItem", back_populates="product")

    @validates("price")
    def validate_price(self, key, value):
        if value <= 0:
            raise ValueError("Price must be greater than 0")
        return value

    @validates("stock")
    def validate_stock(self, key, value):
        if value < 0:
            raise ValueError("Stock cannot be negative")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "image_url": self.image_url,
            "category": self.category,
            "brand": self.brand,
            "stock": self.stock,  # ✅ include in response
            "created_at": self.created_at.isoformat()
        }


# ---------------- CART ITEM ----------------
class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    quantity = db.Column(db.Integer, default=1)

    product = db.relationship("Product", back_populates="cart_items")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "product_name": self.product.name,
            "price": self.product.price,
            "image_url": self.product.image_url,
            "quantity": self.quantity
        }


# ---------------- ORDER ----------------
class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship("OrderItem", backref="order", lazy=True)

    @property
    def total(self):
        return sum(item.product.price * item.quantity for item in self.items)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "items": [i.to_dict() for i in self.items],
            "total": self.total,
            "created_at": self.created_at.isoformat()
        }


# ---------------- ORDER ITEM ----------------
class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    product = db.relationship("Product", back_populates="order_items")

    def to_dict(self):
        return {
            "id": self.id,
            "product": self.product.name,
            "price": self.product.price,
            "image_url": self.product.image_url,
            "quantity": self.quantity
        }
