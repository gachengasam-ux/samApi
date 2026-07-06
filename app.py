from flask import Flask, jsonify, request
# imports ,flask: creates the web app,
# jsonify:turns python data into JSON,
# request: lets you read data sent by the user,like form or JSON input
from inventory import (
    get_all_items,
    get_item_by_id,
    add_item,
    update_item,
    delete_item,
    fetch_product_from_api
)
# creates a flask application object(holds all your routes and tells flask how the app should behave)
app = Flask(__name__)
# ROUTES
# shows all inventory items
@app.route("/items", methods=["GET"])
def get_items():
    # returns list as a JSON with status code 200(success)
    return jsonify(get_all_items()), 200
# looks for one item by id
@app.route("/items/<int:item_id>", methods=["GET"])
def get_single_item(item_id):
    item = get_item_by_id(item_id)
    if item is None:
        # if item does not exist returns a 404 error
        return jsonify({"message": "Item not found"}), 404
# if items exists it returns it
    return jsonify(item), 200
# adds a new inventory item
@app.route("/items", methods=["POST"])
def create_item():
    # reads the JSON body sent by the client
    data = request.get_json()
    #  400 means invalid
    if not data or "name" not in data or "quantity" not in data or "price" not in data:
        return jsonify({"message": "Missing required fields"}), 400

    new_item = add_item(
        data["name"],
        data["quantity"],
        data["price"],
        data.get("barcode")
    )
# request succesfully created
    return jsonify(new_item), 201

# changes only the fields that the user sends
@app.route("/items/<int:item_id>", methods=["PATCH"])
def edit_item(item_id):
    data = request.get_json()
    item = update_item(
        item_id,
        name=data.get("name"),
        quantity=data.get("quantity"),
        price=data.get("price"),
        barcode=data.get("barcode")
    )

    if item is None:
        return jsonify({"message": "Item not found"}), 404

    return jsonify(item), 200

# removes an item from the list
@app.route("/items/<int:item_id>", methods=["DELETE"])
def remove_item(item_id):
    success = delete_item(item_id)

    if not success:
        return jsonify({"message": "Item not found"}), 404

    return jsonify({"message": "Item deleted successfully"}), 200

# external API lookup
# class Open Food Facts using a barcode
@app.route("/external/<string:barcode>", methods=["GET"])
def get_external_product(barcode):
    product = fetch_product_from_api(barcode)
# If external API does not find the product 404 error
    if product is None:
        return jsonify({"message": "Product not found"}), 404
# returns product
    return jsonify(product), 200


if __name__ == "__main__":
    app.run(debug=True)

