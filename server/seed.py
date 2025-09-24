# server/seed.py

from server.app import app, db
from server.models import User, Product, Order, OrderItem, CartItem as Cart
from datetime import datetime, UTC

with app.app_context():
    # Clear old data
    Cart.query.delete()
    OrderItem.query.delete()
    Order.query.delete()
    Product.query.delete()
    User.query.delete()

    # Users
    users = [
        User(username="alice", email="alice@example.com", password="password123"),
        User(username="bob", email="bob@example.com", password="securepass"),
        User(username="charlie", email="charlie@example.com", password="charliepw"),
    ]

    # Products
    products = [
        Product(name="Laptop", price=899.99, category="Electronics",
                details="Powerful laptop with 16GB RAM, 512GB SSD.",
                image="https://via.placeholder.com/150"),
        Product(name="Smartphone", price=499.99, category="Electronics",
                details="Latest model with high-resolution camera.",
                image="https://via.placeholder.com/150"),
        Product(name="Headphones", price=99.99, category="Electronics",
                details="Noise-cancelling over-ear headphones.",
                image="https://via.placeholder.com/150"),
        Product(name="Running Shoes", price=75.00, category="Clothing",
                details="Lightweight and durable running shoes.",
                image="https://via.placeholder.com/150"),
        Product(name="Backpack", price=65.00, category="Fashion",
                details="Stylish and durable backpack for everyday use.",
                image="https://via.placeholder.com/150"),
    ]

    db.session.add_all(users + products)
    db.session.commit()

    # Orders
    order1 = Order(user_id=users[0].id, created_at=datetime.now(UTC))
    order2 = Order(user_id=users[1].id, created_at=datetime.now(UTC))
    db.session.add_all([order1, order2])
    db.session.flush()  # Get IDs

    # OrderItems
    order_items = [
        OrderItem(order_id=order1.id, product_id=products[0].id, quantity=1),
        OrderItem(order_id=order1.id, product_id=products[2].id, quantity=2),
        OrderItem(order_id=order2.id, product_id=products[1].id, quantity=1),
    ]

    db.session.add_all(order_items)

    # Carts
    carts = [
        Cart(user_id=users[0].id, product_id=products[4].id, quantity=1),
        Cart(user_id=users[1].id, product_id=products[3].id, quantity=2),
        Cart(user_id=users[2].id, product_id=products[2].id, quantity=1),
    ]

    db.session.add_all(carts)
    db.session.commit()

    print("Database seeded with Users, Products, Orders, OrderItems, and Carts!")
