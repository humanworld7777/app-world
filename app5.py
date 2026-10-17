import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)
DB_NAME = "inventory.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


@app.route("/")
def home():
    return "Welcome to the SQLite Store API!"


@app.route("/products", methods=["GET"])
def get_all_products():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()

    product_list = [dict(row) for row in products]
    return jsonify({"products": product_list, "count": len(product_list)}), 200


@app.route("/products/<int:item_id>", methods=["GET"])
def get_product(item_id):
    conn = get_db_connection()
    product = conn.execute(
        "SELECT * FROM products WHERE id = ?", (item_id,)
    ).fetchone()
    conn.close()

    if product is None:
        return jsonify({"status": "error", "message": "Product not found"}), 404

    return jsonify(dict(product)), 200


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

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, price) VALUES (?, ?)", (name, price)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return (
        jsonify(
            {
                "status": "success",
                "message": f"Product '{name}' added",
                "product": {"id": new_id, "name": name, "price": price},
            }
        ),
        201,
    )


@app.route("/update-product/<int:item_id>", methods=["PUT"])
def update_product(item_id):
    data = request.get_json() or {}

    conn = get_db_connection()
    product = conn.execute(
        "SELECT * FROM products WHERE id = ?", (item_id,)
    ).fetchone()

    if product is None:
        conn.close()
        return jsonify({"status": "error", "message": "Product not found"}), 404

    new_name = data.get("name", product["name"])
    new_price = data.get("price", product["price"])

    conn.execute(
        "UPDATE products SET name = ?, price = ? WHERE id = ?",
        (new_name, new_price, item_id),
    )
    conn.commit()
    conn.close()

    return (
        jsonify(
            {
                "status": "success",
                "message": f"Product {item_id} updated",
                "product": {"id": item_id, "name": new_name, "price": new_price},
            }
        ),
        200,
    )


@app.route("/delete-product/<int:item_id>", methods=["DELETE"])
def delete_product(item_id):
    conn = get_db_connection()
    product = conn.execute(
        "SELECT * FROM products WHERE id = ?", (item_id,)
    ).fetchone()

    if product is None:
        conn.close()
        return jsonify({"status": "error", "message": "Product not found"}), 404

    conn.execute("DELETE FROM products WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

    return (
        jsonify(
            {
                "status": "success",
                "message": f"Product '{product['name']}' deleted",
            }
        ),
        200,
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5009)
