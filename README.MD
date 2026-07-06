# Inventory Management System

This is a simple Flask REST API for managing inventory items.  
It also connects to the Open Food Facts API to fetch product details by barcode.

## Features

- Add inventory items
- View all items
- View one item by ID
- Update items
- Delete items
- Fetch product details from Open Food Facts
- CLI menu for interacting with the API
- Unit tests for the main features

## Technologies Used

- Python
- Flask
- Requests
- Pytest

## Project Structure

```text
SAMAPI/
├── app.py
├── cli.py
├── inventory.py
├── requirements.txt
├── tests/
│   └── test_app.py
└── README.md
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-github-repo-link>
cd inventory-api
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

## Running Tests

Run the tests with:

```bash
pytest
```

## API Endpoints

- `GET /items` - Get all items
- `GET /items/<id>` - Get one item
- `POST /items` - Add a new item
- `PATCH /items/<id>` - Update an item
- `DELETE /items/<id>` - Delete an item
- `GET /external/<barcode>` - Fetch product data from Open Food Facts

## Example Request

```json
{
  "name": "Rice",
  "quantity": 10,
  "price": 500
}
```

## Notes

This project uses in-memory storage, so items will reset when the server restarts.