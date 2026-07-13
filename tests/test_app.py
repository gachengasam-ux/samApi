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



# GET /external/<barcode>
# requests.get is mocked so these tests never hit the real internet


@patch("inventory.requests.get")
def test_external_product_found(mock_get, client):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Coca Cola",
            "brands": "Coca-Cola",
            "categories": "Beverages"
        }
    }
    response = client.get("/external/5449000000996")
    data = response.get_json()
    assert response.status_code == 200
    assert data["name"] == "Coca Cola"


@patch("inventory.requests.get")
def test_external_product_not_found(mock_get, client):
    mock_get.return_value.status_code = 404
    response = client.get("/external/00000000")
    assert response.status_code == 404



# GET /external/search


@patch("inventory.requests.get")
def test_external_search_by_name(mock_get, client):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "products": [
            {
                "code": "111",
                "product_name": "Basmati Rice",
                "brands": "Brand A",
                "categories": "Grains"
            }
        ]
    }
    response = client.get("/external/search?name=rice")
    data = response.get_json()
    assert response.status_code == 200
    assert data[0]["barcode"] == "111"
    assert data[0]["name"] == "Basmati Rice"


def test_external_search_missing_query(client):
    response = client.get("/external/search")
    assert response.status_code == 400



# POST /external/import
# this is the "insert searched product into current inventory" feature


@patch("inventory.requests.get")
def test_external_import_adds_to_inventory(mock_get, client):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Coca Cola",
            "brands": "Coca-Cola",
            "categories": "Beverages"
        }
    }
    response = client.post("/external/import", json={
        "barcode": "5449000000996",
        "quantity": 10,
        "price": 150
    })
    data = response.get_json()
    assert response.status_code == 201
    assert data["name"] == "Coca Cola"
    assert data["quantity"] == 10
    assert data["barcode"] == "5449000000996"

    # confirm it actually landed in the inventory array, not just returned
    get_response = client.get("/items")
    items = get_response.get_json()
    assert len(items) == 1
    assert items[0]["name"] == "Coca Cola"


def test_external_import_missing_barcode(client):
    response = client.post("/external/import", json={})
    assert response.status_code == 400


@patch("inventory.requests.get")
def test_external_import_product_not_found(mock_get, client):
    mock_get.return_value.status_code = 404
    response = client.post("/external/import", json={"barcode": "00000000"})
    assert response.status_code == 404








