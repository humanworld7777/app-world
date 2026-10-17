from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
  return "Welcome to the store API!"

@app.route("/product/<int;item_id>")
def get_product(item_id):
  return jsonify({"product_id": item_id, "status": "available"})

@app.route("/add-product", methods=['POST'])
def add_product():
  data = request.get_json() or {}
  name = data.get("name")
  price = data.get("price")

  if name and price:
    return jsonify({
      "status": "error",
      "message": "Missing name or price"
    }), 400

if __name__ == "__main__":
  app.run(debug=True)
EOF
