# server/seed.py

import os
from server.app import create_app
from server.models import db, User, Product, CartItem, Order, OrderItem

app = create_app()

with app.app_context():
    print("Seeding database...")

    try:
        # if FORCE_RESEED=1 in environment, drop and recreate everything.
        force = os.environ.get("FORCE_RESEED", "0") == "1"
        if force:
            print("Force reseed enabled: dropping all tables.")
            db.drop_all()

        # ensure tables exist (will create them if they don't)
        db.create_all()

        # --------------------
        # USERS
        # --------------------
        user1 = User(username="Alice", email="alice@example.com", password="password123")
        user2 = User(username="Bob", email="bob@example.com", password="securepass")
        db.session.add_all([user1, user2])
        db.session.commit()
        print("Users seeded.")

        # --------------------
        # PRODUCTS
        # --------------------
        product1 = Product(name="Laptop", price=1200.0)
        product2 = Product(name="Headphones", price=150.0)
        product3 = Product(name="Mouse", price=50.0)
        db.session.add_all([product1, product2, product3])
        db.session.commit()
        print("Products seeded.")

        # --------------------
        # CART ITEMS
        # --------------------
        cart_item1 = CartItem(user_id=user1.id, product_id=product1.id, quantity=1)
        cart_item2 = CartItem(user_id=user1.id, product_id=product2.id, quantity=2)
        cart_item3 = CartItem(user_id=user2.id, product_id=product3.id, quantity=3)
        db.session.add_all([cart_item1, cart_item2, cart_item3])
        db.session.commit()
        print("Cart items seeded.")

        # --------------------
        # ORDERS
        # --------------------
        order1 = Order(user_id=user1.id)
        order2 = Order(user_id=user2.id)
        db.session.add_all([order1, order2])
        db.session.commit()
        print("Orders seeded.")

        # --------------------
        # ORDER ITEMS
        # --------------------
        order_item1 = OrderItem(order_id=order1.id, product_id=product1.id, quantity=1)
        order_item2 = OrderItem(order_id=order1.id, product_id=product2.id, quantity=2)
        order_item3 = OrderItem(order_id=order2.id, product_id=product3.id, quantity=3)
        db.session.add_all([order_item1, order_item2, order_item3])
        db.session.commit()
        print("Order items seeded.")

        print("Database seeded successfully!")

    except Exception as e:
        db.session.rollback()
        print("Failed to seed database:", e)
