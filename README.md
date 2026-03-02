# Stock System CLI

A command-line inventory management system built with Python and SQLite. Register products, track stock levels, update quantities, and delete records — all stored in a local database.

## Features

- Register products with name, quantity, price and category
- List all products with low stock alerts
- Update stock with entry and exit movements
- Delete products
- Data persisted in a local SQLite database

## Requirements

Python 3.10+
No external libraries required

### How to run

```bash
python stock_system.py
```

### Project structure

```bash
stock_system/
├── stock_system.py # Main application
└── stock.db # SQLite database (auto-created on first run)
```

## Learned

- Object-oriented programming with classes in Python
- SQLite database operations (CREATE, INSERT, SELECT, UPDATE, DELETE)
- Separating concerns between data and business logic
