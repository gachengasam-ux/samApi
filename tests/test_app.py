# imports
# testing library
import pytest
# mocking library so tests never make real network calls to Open Food Facts
from unittest.mock import patch
# Flask app so the test can use it
from app import app
# Import the reset helper so both the inventory list AND the id counter
# get cleared between tests (fixes ids drifting upward across test runs)
from inventory import reset_inventory

# client fixture
# create reusable test data
@pytest.fixture
def client():
    # Flask running in test mode
    app.config["TESTING"] = True
    # fake client for sending requests to the app
    with app.test_client() as client:
        # gives that client to each test that needs it
        yield client

# Clear inventory fixture
# fixture will run automatically for each test
@pytest.fixture(autouse=True)
def clear_inventory():
    # empties the list AND resets the id counter before a test starts
    reset_inventory()
    # lets the test run
    yield
    # runs again after test cleanup
    reset_inventory()



# GET /items


# test for empty list
def test_get_all_items_empty(client):
    response = client.get("/items")
    assert response.status_code == 200
    assert response.get_json() == []



# POST /items


# test for creating an item
def test_create_item(client):
    response = client.post("/items", json={
        "name": "Rice",
        "quantity": 10,
        "price": 500
    })
    data = response.get_json()
    assert response.status_code == 201
    assert data["name"] == "Rice"
    assert data["quantity"] == 10
    assert data["price"] == 500


# missing required field should be rejected, not silently accepted
def test_create_item_missing_fields(client):
    response = client.post("/items", json={"name": "Rice"})
    assert response.status_code == 400
    assert "message" in response.get_json()


# GET /items/<id>


def test_get_single_item(client):
    client.post("/items", json={
        "name": "Sugar",
        "quantity": 5,
        "price": 200
    })
    response = client.get("/items/1")
    data = response.get_json()
    assert response.status_code == 200
    assert data["name"] == "Sugar"


def test_item_not_found(client):
    response = client.get("/items/99")
    assert response.status_code == 404



# PATCH /items/<id>


def test_update_item(client):
    client.post("/items", json={
        "name": "Milk",
        "quantity": 2,
        "price": 150
    })
    response = client.patch("/items/1", json={
        "quantity": 4
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data["quantity"] == 4


# patching an item that doesn't exist should 404, not crash
def test_update_item_not_found(client):
    response = client.patch("/items/999", json={"quantity": 5})
    assert response.status_code == 404


# DELETE /items/<id>


def test_delete_item(client):
    client.post("/items", json={
        "name": "Bread",
        "quantity": 3,
        "price": 100
    })
    response = client.delete("/items/1")
    data = response.get_json()
    assert response.status_code == 200
    assert data["message"] == "Item deleted successfully"


def test_delete_item_not_found(client):
    response = client.delete("/items/999")
    assert response.status_code == 404







