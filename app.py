from flask import Flask, reques, jsonify
app = Flask(__name__)
@app.route("/login", methods=['GET', "POST"])
def login():
  if request.method == 'POST':
    data = request.get_json()
    username = data.get("username", "Guest")
    password = data.get("password", "")

if username == "admin" and password == "secret123":
  return jsonify({"status": "sucess", "message": f"Welcome back, {username}!"})
else:
  return jsonify({"status": "error", "message": "Invalid credential"}), 401

if __name__ == "__main__":
  app.run(debug=True, port=5009)
  
