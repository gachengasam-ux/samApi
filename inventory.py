import requests
# initialization
# items are stored in an empty array
inventory = []
# giving each item a unique number
next_id = 1


# giving back the whole inventory list since inventory stores all items
def get_all_items():
    return inventory
# Look whose id matches the number you pass
def get_item_by_id(item_id):
    # looping through each dictionary in the list checking for item"id"
    for item in inventory:
        if item["id"] == item_id:
            # returns item as soon as it finds a match
            return item
    return None

#creating a new dictionary and then we put them in a list

def add_item(name, quantity, price, barcode=None):
    global next_id

    item = {
        "id": next_id,
        "name": name,
        "quantity": quantity,
        "price": price,
        "barcode": barcode

    }
    inventory.append(item)
    next_id += 1
    return item

# update an item : to change the fields that you provide
def update_item(item_id, name=None, quantity=None, price=None, barcode=None):
    item = get_item_by_id(item_id)

    if item is None:
        return None
    if name is not None:
        item["name"] = name
    if quantity is not None:
        item["quantity"] = quantity
    if price is not None:
        item["price"] = price
    if barcode is not None:
        item["barcode"] = barcode

    return item

# delete item : if the item exists
def delete_item(item_id):
    item = get_item_by_id(item_id)

    if item is None:
        return False

    inventory.remove(item)
    return True

# sending a request to Open Food Facts and reads the JSON response
def fetch_product_from_api(barcode):
    url = f"https://world.openfoodfacts.net/api/v2/product/{barcode}.json"
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return None

    data = response.json()

    if data.get("status") != 1:
        return None

    product = data.get("product", {})

    return {
        "name": product.get("product_name", "Unknown Product"),
        "brand": product.get("brands", "Unknown Brand"),
        "category": product.get("categories", "Unknown Category"),
        "barcode": barcode
    }

