# Inventory Management System

This is a simple Flask REST API for managing inventory items.
It also connects to the Open Food Facts API to search for products by
barcode or name, and to import a found product straight into the
current inventory.

## Features

- Add inventory items
- View all items
- View one item by ID
- Update items (partial update via PATCH)
- Delete items
- Search Open Food Facts by barcode
- Search Open Food Facts by product name (returns multiple candidates)
- Import a searched product directly into inventory
- CLI menu for interacting with the API
- Unit tests for all routes, including mocked external API calls

## Technologies Used

- Python
- Flask
- Requests
- Pytest

## Project Structure

```text
samApi/
├── app.py
├── cli.py
├── inventory.py
├── conftest.py
├── requirements.txt
├── tests/
│   └── test_app.py
└── README.md
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone git@github.com:gachengasam-ux/samApi.git
cd samApi
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

On Windows:

```bash
py -3 -m venv .venv
```

### 3. Activate the virtual environment

On Mac/Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Flask App

Start the Flask server with:

```bash
python app.py
```

The API will run at:

```text
http://127.0.0.1:5000
```

## Running the CLI

Make sure the Flask app is running first, then in another terminal run:

```bash
python cli.py
```

The CLI lets you view, add, update, and delete inventory items, and also
search Open Food Facts by barcode or name and insert the result straight
into inventory (menu option 5).

## Running Tests

Run the tests with:

```bash
pytest
```

Tests cover all CRUD routes (including not-found and missing-field cases)
and all external API routes, using mocked HTTP calls so they never depend
on a live internet connection.

## API Endpoints

| Method | Route                     | Description                                                 |
|--------|---------------------------|---------------------------------------------------------------|
| GET    | `/items`                  | Get all inventory items                                       |
| GET    | `/items/<id>`              | Get a single item by ID                                       |
| POST   | `/items`                  | Add a new item (`name`, `quantity`, `price` required)          |
| PATCH  | `/items/<id>`              | Update one or more fields on an existing item                  |
| DELETE | `/items/<id>`              | Delete an item                                                 |
| GET    | `/external/<barcode>`      | Look up a single product on Open Food Facts by barcode          |
| GET    | `/external/search?name=`   | Search Open Food Facts by product name, returns candidates      |
| POST   | `/external/import`         | Fetch a product by barcode and insert it into inventory         |

## Example Requests

Create an item directly:

```json
POST /items
{
  "name": "Rice",
  "quantity": 10,
  "price": 500
}
```

Search Open Food Facts by name:

```text
GET /external/search?name=rice
```

Import a searched product into inventory:

```json
POST /external/import
{
  "barcode": "5449000000996",
  "quantity": 10,
  "price": 150
}
```

## Notes

This project uses in-memory storage, so items will reset when the server
restarts.