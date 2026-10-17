import os
import tempfile
import pytest
from app6 import app, db, Product

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

    os.close(db_fd)
    os.unlink(db_path)

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the SQLAlchemy Store API!" in response.data

def test_add_product(client):
    response = client.post("/add_product", json={"name": "Wireless Mouse", "price": 29.99})
    assert response.status_code == 201
    data = response.get_json()
    assert data["status"] == "success"
    assert data["product"]["name"] == "Wireless Mouse"

def test_get_products(client):
    client.post("/add_product", json={"name": "Keyboard", "price": 79.99})
    response = client.get("/products")
    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == 1
    assert data["products"][0]["name"] == "Keyboard"

def test_update_product(client):
    client.post("/add_product", json={"name": "Monitor", "price": 200.00})
    response = client.put("/update-product/1", json={"price": 180.00})
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["product"]["price"] == 180.00

def test_delete_product(client):
    client.post("/add_product", json={"name": "Old Item", "price": 10.00})
    response = client.delete("/delete-product/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "deleted" in data["message"]
