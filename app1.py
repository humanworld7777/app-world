from flask import Flask, request, jsonify
app = Flask(__name__)
@app.route("/")
def home():

@app.route("/product/<int:item_id>")
def get_product(item_id):
  return jsonify({"product_id": item_id, "status": "available"})


@app.route("/add-product", methods=(['PosT'])
def add_product():
  if __name__ == "__main__":
    app.run(debug=True)
