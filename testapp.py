import pytest
from app import app, db, User

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["status"] == "success"

def test_register_and_login(client):
    reg_response = client.post("/register", json={
        "username": "testuser",
        "password": "password123"
    })
    assert reg_response.status_code == 200
    assert reg_response.json["status"] == "success"

    login_response = client.post("/login", json={
        "username": "testuser",
        "password": "password123"
    })
    assert login_response.status_code == 200
    assert login_response.json["status"] == "success"

    bad_login = client.post("/login", json={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert bad_login.status_code == 401
    assert bad_login.json["status"] == "error"

def test_profile(client):
    client.post("/register", json={
        "username": "profileuser",
        "password": "password123"
    })

    profile_response = client.post("/profile", json={
        "username": "profileuser"
    })
    assert profile_response.status_code == 200
    assert profile_response.json["profile"]["username"] == "profileuser"
