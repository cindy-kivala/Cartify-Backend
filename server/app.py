from flask import Flask, request, jsonify
from flask_migrate import Migrate
from server.models import db, Product, Order

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)



@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "price": p.price} for p in products])

@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({"id": product.id, "name": product.name, "price": product.price})

@app.route("/products", methods=["POST"])
def create_product():
    data = request.json
    try:
        new_product = Product(name=data["name"], price=data["price"])
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"id": new_product.id, "name": new_product.name, "price": new_product.price}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/products/<int:id>", methods=["PATCH"])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.json
    if "name" in data:
        product.name = data["name"]
    if "price" in data:
        product.price = data["price"]
    db.session.commit()
    return jsonify({"id": product.id, "name": product.name, "price": product.price})

@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 200



@app.route("/orders", methods=["POST"])
def create_order():
    data = request.json
    order = Order(
        user_name=data["user_name"],
        product_id=data["product_id"],
        quantity=data.get("quantity", 1)
    )
    db.session.add(order)
    db.session.commit()
    return jsonify({
        "id": order.id,
        "user_name": order.user_name,
        "product_id": order.product_id,
        "quantity": order.quantity
    }), 201

@app.route("/orders/<string:username>", methods=["GET"])
def get_orders(username):
    orders = Order.query.filter_by(user_name=username).all()
    return jsonify([
        {
            "id": o.id,
            "user_name": o.user_name,
            "product": o.product.name,
            "quantity": o.quantity,
            "price": o.product.price
        }
        for o in orders
    ])



if __name__ == "__main__":
    app.run(debug=True)
