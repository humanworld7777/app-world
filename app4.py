
from flask import Flask, request, jsonify

app = Flask(__name__)

products = []

@app.route("/")
def home():
    return "Welcome to the Store API!"

@app.route("/products", methods=['GET'])
def get_all_products():
    return jsonify({"products": products, "count": len(products)})

@app.route("/product/<int:item_id>", methods=['GET'])
def get_product(item_id):
    for item in products:
        if item["id"] == item_id:
            return jsonify(item), 200
    return jsonify({"status": "error", "message": "Product not found"}), 404

@app.route("/add-product", methods=['POST'])
def add_product():
    data = request.get_json() or {}
    name = data.get("name")
    price = data.get("price")
    
    if name and price:
        new_id = len(products) + 1
        new_product = {"id": new_id, "name": name, "price": price}
        products.append(new_product)
        return jsonify({"status": "success", "message": f"Product '{name}' added", "product": new_product}), 201
    return jsonify({"status": "error", "message": "Missing name or price"}), 400

@app.route("/update-product/<int:item_id>", methods=['PUT'])
def update_product(item_id):
    data = request.get_json() or {}
    for item in products:
        if item["id"] == item_id:
            item["name"] = data.get("name", item["name"])
            item["price"] = data.get("price", item["price"])
            return jsonify({"status": "success", "message": f"Product {item_id} updated", "product": item}), 200
    return jsonify({"status": "error", "message": "Product not found"}), 404

@app.route("/delete-product/<int:item_id>", methods=['DELETE'])
def delete_product(item_id):
    for index, item in enumerate(products):
        if item["id"] == item_id:
            deleted_item = products.pop(index)
            return jsonify({"status": "success", "message": f"Product '{deleted_item['name']}' deleted"}), 200
    return jsonify({"status": "error", "message": "Product not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5009)
