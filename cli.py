import requests
# address to your local api
BASE_URL = "http://127.0.0.1:5000"

# menu fucntion: to print the options
# print : to display the menu in the terminal
def show_menu():
    print("\n=== Inventory CLI ===")
    print("1. View all items")
    print("2. Add item")
    print("3. Update item")
    print("4. Delete item")
    print("5. Fetch product from Open Food Facts")
    print("6. Exit")

# view items function
def view_items():
    # sends a GET request to /items
    response = requests.get(f"{BASE_URL}/items")
    # print the data returned by the api
    print(response.json())
# 1
# Add item function
def add_item():
    # asks the user for item details
    name = input("Enter name: ")
    # convert the text input into the right types
    quantity = int(input("Enter quantity: "))
    price = float(input("Enter price: "))
    barcode = input("Enter barcode (optional): ")
# dictionary for the JSON body
    data = {
        "name": name,
        "quantity": quantity,
        "price": price
    }
    if barcode:
        data["barcode"] = barcode
# a new item is sent to the API
    response = requests.post(f"{BASE_URL}/items", json=data)
    print(response.json())

# 2
# Update item function
def update_item():
    # asks which item to update
    item_id = input("Enter item ID: ")
    # change here only the fields you want
    name = input("Enter new name (leave blank to skip): ")
    quantity = input("Enter new quantity (leave blank to skip): ")
    price = input("Enter new price (leave blank to skip): ")
# empty dictionary initially
    data = {}
# checks only the values that were typed
    if name:
        data["name"] = name
    if quantity:
        data["quantity"] = int(quantity)
    if price:
        data["price"] = float(price)
# sends the update to the server
    response = requests.patch(f"{BASE_URL}/items/{item_id}", json=data)
    print(response.json())

# 3
# delete item
def delete_item():
    # asks for the id of the item to remove
    item_id = input("Enter item ID: ")
    # sends a delete request to the API
    response = requests.delete(f"{BASE_URL}/items/{item_id}")
    # prints the confirmation message
    print(response.json())

# external product lookup: connects external API feature in your project
def fetch_external_product():
    # user enters barcode
    barcode = input("Enter barcode: ")
    # CLI sends a GET request to your flask route then flask talks to open food facts behind the scenes
    response = requests.get(f"{BASE_URL}/external/{barcode}")
    print(response.json())

# Main loop
def main():
    # keeps the menu running until user exits
    while True:
        show_menu()
        # read the selected menu option
        choice = input("Choose an option: ")
        # if and elif send the user to the corect function
        if choice == "1":
            view_items()
        elif choice == "2":
            add_item()
        elif choice == "3":
            update_item()
        elif choice == "4":
            delete_item()
        elif choice == "5":
            fetch_external_product()
        elif choice == "6":
            print("Goodbye!")
            # stops the loop when the user chooses to exit
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()


