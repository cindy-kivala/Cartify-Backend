from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from server.models import db, Product, User, Order, OrderItem, CartItem as CartItemModel

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
CORS(app, origins=["http://localhost:5173"])

#Routes
@app.route("/")
def home():
    return "<h1>Welcome to Cartify API!</h1>", 200


# 1. Products
class ProductList(Resource):
    def get(self):
        products = Product.query.all()
        return [p.to_dict() for p in products], 200

    def post(self):
        data = request.get_json() or {}
        if not data.get("name") or not data.get("price"):
            return {"error": "Missing required fields: 'name' and 'price'"}, 400

        try:
            product = Product(
            name=data["name"],
            price=data["price"],
            category=data.get("category"),
            details=data.get("details")
        )
            db.session.add(product)
            db.session.commit()
            return product.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400


class ProductResource(Resource):
    def get(self, id):
        product = Product.query.get_or_404(id)
        return product.to_dict(), 200

    def patch(self, id):
        product = Product.query.get_or_404(id)
        data = request.get_json() or {}
        if "name" in data:
            product.name = data["name"]
        if "price" in data:
            product.price = data["price"]
        if "category" in data:
            product.category = data["category"]
        if "details" in data:
            product.details = data["details"]

        db.session.commit()
        return product.to_dict(), 200

    def delete(self, id):
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted"}, 200



# 2. Orders
class OrderList(Resource):
    def get(self):
        orders = Order.query.all()
        return [o.to_dict() for o in orders], 200

    def post(self):
        data = request.get_json() or {}
        if not data.get("user_id") or not data.get("items"):
            return {"error": "Missing required fields: 'user_id' and 'items'"}, 400

        try:
            order = Order(user_id=data["user_id"])
            db.session.add(order)
            db.session.commit()  # commit first to get order.id

            for item in data.get("items", []):
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item["product_id"],
                    quantity=item.get("quantity", 1),
                )
                db.session.add(order_item)

            db.session.commit()
            return {"id": order.id, "total": order.total}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400


class OrderResource(Resource):
    def get(self, id):
        order = Order.query.get_or_404(id)
        return order.to_dict(), 200

    def delete(self, id):
        order = Order.query.get_or_404(id)
        db.session.delete(order)
        db.session.commit()
        return {"message": "Order deleted"}, 200



# 3. Users
class UserList(Resource):
    def get(self):
        users = User.query.all()
        return [u.to_dict() for u in users], 200

    def post(self):
        data = request.get_json() or {}
        required = ["username", "email", "password"]
        missing = [field for field in required if field not in data]
        if missing:
            return {"error": f"Missing required fields: {', '.join(missing)}"}, 400

        try:
            user = User(username=data["username"], email=data["email"])
            user.password = data["password"]
            db.session.add(user)
            db.session.commit()
            return user.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400


# 4. Cart Items
class CartList(Resource):
    def get(self, user_id):
        cart_items = CartItemModel.query.filter_by(user_id=user_id).all()
        return [item.to_dict() for item in cart_items], 200

    def post(self, user_id):
        # Add product to cart
        data = request.get_json() or {}
        product_id = data.get("product_id")
        if not product_id:
            return {"error": "Missing required field: 'product_id'"}, 400

        try:
            # Check if the product is already in the user's cart
            existing_item = CartItemModel.query.filter_by(
                user_id=user_id, 
                product_id=data["product_id"]
            ).first()

            if existing_item:
                # Increment the quantity
                existing_item.quantity += data.get("quantity", 1)
                db.session.commit()
                return existing_item.to_dict(), 200
            else:
                # Add new cart item
                item = CartItemModel(
                    user_id=user_id,
                    product_id=data["product_id"],
                    quantity=data.get("quantity", 1)
                )
                db.session.add(item)
                db.session.commit()
                return item.to_dict(), 201

        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400

class CartItemResource(Resource):
    def patch(self, user_id, cart_item_id):
        item = CartItemModel.query.filter_by(user_id=user_id, id=cart_item_id).first_or_404()
        data = request.get_json() or {}
        if "quantity" in data:
            item.quantity = data["quantity"]
        db.session.commit()
        return item.to_dict(), 200

    def delete(self, user_id, cart_item_id):
        item = CartItemModel.query.filter_by(user_id=user_id, id=cart_item_id).first_or_404()
        db.session.delete(item)
        db.session.commit()
        return {"message": "Cart item deleted"}, 200



# Register resources
api.add_resource(ProductList, "/products")
api.add_resource(ProductResource, "/products/<int:id>")

api.add_resource(OrderList, "/orders")
api.add_resource(OrderResource, "/orders/<int:id>")

api.add_resource(UserList, "/users")

api.add_resource(CartList, "/cart/<int:user_id>")
api.add_resource(CartItemResource, "/cart/<int:user_id>/<int:cart_item_id>")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
