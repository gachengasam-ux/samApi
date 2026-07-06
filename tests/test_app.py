# imports
# testing library
import pytest
# Flask app so the test can use it
from app import app
# Import the list where items are stored so the test can clear it between runs
from inventory import inventory

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
    # empties the list before a test starts
    inventory.clear()
    # lets the test run
    yield
    # runs again after test cleanup
    inventory.clear()

# test for empty list
# define a test and it will use the client fixture
def test_get_all_items_empty(client):
    # send a fake GET request to /items
    response = client.get("/items")
    # check if the request has worked
    assert response.status_code == 200
    # checks that the return data is in an empty list
    assert response.get_json() == []

# test for creating an item
def test_create_item(client):
    # sending a POST request with JSON data
    response = client.post("/items", json={
        "name": "Rice",
        "quantity": 10,
        "price": 500

    })
    # saving the returned json
    data = response.get_json()
    # item created successfully
    assert response.status_code == 201
    assert data["name"] == "Rice"
    assert data["quantity"] == 10
    assert data["price"] == 500

# test to get one item
# first an item is created so there is something to fetch
def test_get_single_item(client):
    
    client.post("/items", json={
        "name": "Sugar",
        "quantity": 5,
        "price": 200
    })
# asks for item ID 1
    response = client.get("/items/1")
    data = response.get_json()
# successfully
    assert response.status_code == 200
# correct item came back
    assert data["name"] == "Sugar"
# test update item
# creates an item first
def test_update_item(client):
    client.post("/items", json={
        "name": "Milk",
        "quantity": 2,
        "price": 150
    })
# patch request to change the only quantity
    response = client.patch("/items/1", json={
        "quantity": 4
    })
    data = response.get_json()
# successfully
    assert response.status_code == 200
# checks the value changed
    assert data["quantity"] == 4

# test delete item
# creates an item
def test_delete_item(client):
    client.post("/items", json={
        "name": "Bread",
        "quantity": 3,
        "price": 100
    })
# delete request
    response = client.delete("/items/1")
    data = response.get_json()
# successfully
    assert response.status_code == 200
# confirms if the item was removed
    assert data["message"] == "Item deleted successfully"

# test not found
# asks for an item that does not exist
def test_item_not_found(client):
    response = client.get("/items/99")
    # 404 error not found
    assert response.status_code == 404


