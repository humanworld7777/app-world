from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return jsonify({"status": "success", "message": "Welcome to my Flask API!"})

@app.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"status": "error", "message": "Username and password required"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"status": "error", "message": "User already exists"}), 400

    new_user = User(username=data["username"], password=data["password"])
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"status": "success", "message": f"User {data['username']} registered successfully!"})

@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No JSON data provided"}), 400
        
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({"status": "success", "message": f"Welcome back, {username}!"})
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

if __name__ == "__main__":
    app.run(debug=True, port=5009)
