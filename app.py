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
    fetch_product_from_api,
    search_products_by_name,
    import_product_from_api
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


# search Open Food Facts by product name and barcode
# returns a list of candidates the user can choose from before importing
@app.route("/external/search", methods=["GET"])
def search_external_products():
    name = request.args.get("name")

    if not name:
        return jsonify({"message": "Query parameter 'name' is required"}), 400

    results = search_products_by_name(name)
    return jsonify(results), 200


# takes a barcode found via /external/<barcode> or /external/search
# and inserts it into the current inventory as a real item
@app.route("/external/import", methods=["POST"])
def import_external_product():
    data = request.get_json()

    if not data or "barcode" not in data:
        return jsonify({"message": "barcode is required"}), 400

    barcode = data["barcode"]
    quantity = data.get("quantity", 0)
    price = data.get("price", 0)

    new_item = import_product_from_api(barcode, quantity, price)

    if new_item is None:
        return jsonify({"message": "Product not found"}), 404

    return jsonify(new_item), 201


if __name__ == "__main__":
    app.run(debug=True)

