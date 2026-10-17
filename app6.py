from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///inventory_orm.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price}


@app.route("/")
def home():
    return "Welcome to the SQLAlchemy Store API!"



@app.route("/products", methods=["GET"])
def get_all_products():
    products = Product.query.all()
    product_list = [product.to_dict() for product in products]
    return (
        jsonify({"products": product_list, "count": len(product_list)}),
        200,
    )



@app.route("/products/<int:item_id>", methods=["GET"])
def get_product(item_id):
    product = Product.query.get(item_id)
    if not product:
        return jsonify({"status": "error", "message": "Product not found"}), 404

    return jsonify(product.to_dict()), 200



@app.route("/add_product", methods=["POST"])
def add_product():
    data = request.get_json() or {}
    name = data.get("name")
    price = data.get("price")

    if not name or price is None:
        return (
            jsonify({"status": "error", "message": "Missing name or price"}),
            400,
        )

    new_product = Product(name=name, price=price)
    db.session.add(new_product)
    db.session.commit()

    return (
        jsonify(
            {
                "status": "success",
                "message": f"Product '{name}' added",
                "product": new_product.to_dict(),
            }
        ),
        201,
    )



@app.route("/update-product/<int:item_id>", methods=["PUT"])
def update_product(item_id):
    product = Product.query.get(item_id)
    if not product:
        return jsonify({"status": "error", "message": "Product not found"}), 404

    data = request.get_json() or {}
    product.name = data.get("name", product.name)
    product.price = data.get("price", product.price)

    db.session.commit()

    return (
        jsonify(
            {
                "status": "success",
                "message": f"Product {item_id} updated",
                "product": product.to_dict(),
            }
        ),
        200,
    )



@app.route("/delete-product/<int:item_id>", methods=["DELETE"])
def delete_product(item_id):
    product = Product.query.get(item_id)
    if not product:
        return jsonify({"status": "error", "message": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()

    return (
        jsonify(
            {
                "status": "success",
                "message": f"Product '{product.name}' deleted",
            }
        ),
        200,
    )


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5009)
