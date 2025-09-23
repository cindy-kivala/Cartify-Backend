# server/seed.py

from server.app import create_app
from server import db
from server.models import User, Product, CartItem, Order, OrderItem


app = create_app()

with app.app_context():
    print("Seeding database...")

    # Clear existing data
    db.drop_all()
    db.create_all()

    # USERS
    user1 = User(name="Alice", email="alice@example.com", password="password123")
    user2 = User(name="Bob", email="bob@example.com", password="securepass")
    db.session.add_all([user1, user2])
    db.session.commit()

    # PRODUCTS
    product1 = Product(name="Laptop", price=1200.0)
    product2 = Product(name="Headphones", price=150.0)
    product3 = Product(name="Mouse", price=50.0)
    db.session.add_all([product1, product2, product3])
    db.session.commit()

    # CART ITEMS
    cart_item1 = CartItem(user_id=user1.id, product_id=product1.id, quantity=1)
    cart_item2 = CartItem(user_id=user1.id, product_id=product2.id, quantity=2)
    cart_item3 = CartItem(user_id=user2.id, product_id=product3.id, quantity=3)
    db.session.add_all([cart_item1, cart_item2, cart_item3])
    db.session.commit()

    # ORDERS
    order1 = Order(user_id=user1.id, total_amount=product1.price * 1 + product2.price * 2)
    order2 = Order(user_id=user2.id, total_amount=product3.price * 3)
    db.session.add_all([order1, order2])
    db.session.commit()

    # ORDER ITEMS
    order_item1 = OrderItem(order_id=order1.id, product_id=product1.id, quantity=1, price=product1.price)
    order_item2 = OrderItem(order_id=order1.id, product_id=product2.id, quantity=2, price=product2.price)
    order_item3 = OrderItem(order_id=order2.id, product_id=product3.id, quantity=3, price=product3.price)
    db.session.add_all([order_item1, order_item2, order_item3])
    db.session.commit()

    print("Database seeded successfully!")