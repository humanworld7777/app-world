from flask import Flask, request, jsonify

app = Flask(__name__)

products = []

@app.route("/")
def home():
  return "Welcome to the APEX store"

@app.route("/products", methods=['GET'])
def get_all_products():
  return jsonify({"products": products, "count":
                 len(products)})

@app.route("/product/<int:item_id>", methods=['GET'])
def get_product(item_id):
  for item in products:
    if item["id"] == item_id:
      return jsonify(item), 200
  return jsonify({"status": "error", "message": "Product not found"}), 404

@app.route("/add-product", methods=['POST'])
def add_product():
  data = request.get_json() or {} # Fixed
  name = data.get("name")
  price = data.get("price")

  if name and price:
    new_id = len(products) + 1
    new_product = {
            "id": new_id, 
            "name": name,
            "price": price,
    }
    products.append(new_product)
    return  jsonify({
        "status": "sucess",
        "message": f"Product '{name}' added sucessfully",
        "product": new_product
    }), 201
else: 
   return jsonify({
       "status": "error",
       "message": "Missing name or price"
  })

if __name__ == "__main__":
  app.run(debug=True, port=5009)
  
