# server/seed.py
import os
from server.app import create_app
from server import db
from server.models import User, Product, CartItem, Order, OrderItem

app = create_app()

with app.app_context():
    print("Seeding database...")

    # if FORCE_RESEED=1 in environment, drop and recreate everything.
    force = os.environ.get("FORCE_RESEED", "0") == "1"
    if force:
        print("Force reseed enabled: dropping all tables.")
        db.drop_all()

    # ensure tables exist (will create them if they don't)
    db.create_all()

    # Only seed if no products found (safe guard)
    if Product.query.first() and not force:
        print("Data already present — skipping seed.")
    else:
        try:
            # USERS
            user1 = User(name="Alice", email="alice@example.com", password="password123")
            user2 = User(name="Bob", email="bob@example.com", password="securepass")
            db.session.add_all([user1, user2])
            db.session.commit()
            print("Users seeded.")

            # PRODUCTS
            product1 = Product(name="Laptop", price=1200.0)
            product2 = Product(name="Headphones", price=150.0)
            product3 = Product(name="Mouse", price=50.0)
            db.session.add_all([product1, product2, product3])
            db.session.commit()
            print("Products seeded.")

            # CART ITEMS (optional: attempt and continue if models differ)
            try:
                cart_item1 = CartItem(user_id=user1.id, product_id=product1.id, quantity=1)
                cart_item2 = CartItem(user_id=user1.id, product_id=product2.id, quantity=2)
                cart_item3 = CartItem(user_id=user2.id, product_id=product3.id, quantity=3)
                db.session.add_all([cart_item1, cart_item2, cart_item3])
                db.session.commit()
                print("Cart items seeded.")
            except Exception as e:
                db.session.rollback()
                print("Skipping cart items (model mismatch?):", e)

            # ORDERS and ORDER ITEMS (attempt, but continue if model fields differ)
            try:
                order1 = Order(user_id=getattr(user1, "id", None), total_amount=product1.price * 1 + product2.price * 2)
                order2 = Order(user_id=getattr(user2, "id", None), total_amount=product3.price * 3)
                db.session.add_all([order1, order2])
                db.session.commit()

                order_item1 = OrderItem(order_id=order1.id, product_id=product1.id, quantity=1, price=product1.price)
                order_item2 = OrderItem(order_id=order1.id, product_id=product2.id, quantity=2, price=product2.price)
                order_item3 = OrderItem(order_id=order2.id, product_id=product3.id, quantity=3, price=product3.price)
                db.session.add_all([order_item1, order_item2, order_item3])
                db.session.commit()
                print("Orders and order items seeded.")
            except Exception as e:
                db.session.rollback()
                print("Skipping orders/order items (model mismatch?):", e)

            print("Database seeded successfully!")
        except Exception as outer_e:
            db.session.rollback()
            print("Failed to seed database:", outer_e)
