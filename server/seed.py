# server/seed.py

from server.app import app
from server.models import db, User, Product, CartItem, Order, OrderItem


with app.app_context():
    print("Seeding database...")

    # Clear existing data
    db.drop_all()
    db.create_all()

    # USERS
    user1 = User(username="Alice", email="alice@example.com")
    user1.password = "password123"  # use the setter
    user2 = User(username="Bob", email="bob@example.com")
    user2.password = "securepass"
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
    order1 = Order(user_id=user1.id)
    order2 = Order(user_id=user2.id)
    db.session.add_all([order1, order2])
    db.session.commit()

    # ORDER ITEMS
    order_item1 = OrderItem(order_id=order1.id, product_id=product1.id, quantity=1)
    order_item2 = OrderItem(order_id=order1.id, product_id=product2.id, quantity=2)
    order_item3 = OrderItem(order_id=order2.id, product_id=product3.id, quantity=3)
    db.session.add_all([order_item1, order_item2, order_item3])
    db.session.commit()


    print("Database seeded successfully!")