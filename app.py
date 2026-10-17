from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "success", "message": "Welcome to my Flask API!"})

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No JSON data provided"}), 400
            
        username = data.get("username", "Guest")
        password = data.get("password", "")

        if username == "admin" and password == "secret123":
            return jsonify({"status": "success", "message": f"Welcome back, {username}!"})
        else:
            return jsonify({"status": "error", "message": "Invalid credential"}), 401
            
    return jsonify({"status": "info", "message": "Please send a POST request with username and password"})

if __name__ == "__main__":
    app.run(debug=True, port=5009)
