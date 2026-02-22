import sqlite3 as sql
from datetime import date

file = "stock.db"

class Product:
    def __init__ (self,name, quantity, price, category):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.category = category
        self.created_in = date.today().isoformat()

    
    def __str__(self):
        return f"{self.name}\nQuantity:{self.quantity} | Price: {self.price}\nCategory: {self.category}"

    
def create_connection():
        try:
            connection = sql.connect(file)
            return connection
        except sql.Error:
            print("Error connecting to database.")
            return None

 
def create_table():
    connection = create_connection()
    if connection is None:
        return
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                quantity INTEGER,
                price REAL,
                category TEXT,
                created_in TEXT
            )
        """)
        connection.commit()
    except sql.Error:
        print("Error creating table.")
    finally:
        connection.close()


def register_product():
    try:
        name = str(input("Product name: ").strip())
        quantity = int(input("Quantity: ").strip())
        price = float(input("Price: ").strip())
        category = str(input("Category: ").strip())
    except ValueError:
        print("Type only numbers.")

    product = Product(name, quantity, price, category)
    connection = create_connection()
    if connection is None:
        return
    try:
        cursor = connection.cursor()
        cursor.execute(""" INSERT INTO products (name, quantity, price, category, created_in) VALUES (?, ?, ?, ?, ?)""",
            ( product.name, product.quantity, product.price, product.category, product.created_in))
        connection.commit()
    except sql.Error as e:
        print(f"Error: {e}")
    finally:
        connection.close()


def list_products():
    connection = create_connection()
    if connection is None:
        return
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()

        if not rows:
            print("No products registered yet.")

        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]} | Quantity: {row[2]} | Price: {row[3]} | Category: {row[4]} | Created in: {row[5]}")

    except sql.Error as e:
        print(f"Error: {e}")
    finally:
        connection.close()


def request_id(action):
    try:
        product_id = int(input(f"Enter the product ID you want to {action}: ").strip())
        return product_id
    except ValueError:
        print("Invalid ID, Type only numbers.")
        return None


def update_stock():
    list_products()
    product_id = request_id("update")
    if product_id is None:
        return 
    
    print("1 - Stock entry\n2 - Stock exit")
    try:
        option = int(input("Choose (1-2): ").strip())
    except ValueError:
        print("Invalid option.")
        return
    
    if option not in [1, 2]:
        print("Invalid option")
        return
    
    connection = create_connection()
    if connection is None:
        return
    
    try:
        amount = int(input("Quantity: ").strip())
    except ValueError:
        print("Type only numbers.")
        return
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products WHERE ID = ?", (product_id))
        row = cursor.fetchone()
        if not row:
            print("Product not found.")
            return
    
        current_quantity = row[2]
        if option == 1:
            new_quantity = current_quantity + amount
        else:
            new_quantity = current_quantity - amount
        cursor.execute("UPDATE products SET QUANTITY = ? WHERE id = ?", (new_quantity, product_id))
        connection.commit()
        print("Stock updated.")
    except sql.Error as e:
        print(f"Error: {e}")
    finally:
        connection.close()


def delete_product():
    list_products()
    product_id = request_id("delete")
    if product_id is None:
        return
    
    connection = create_connection()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        if not row:
            print("Product not found.")
            return
        confirmation = str(input(f"Are you sure you want to delete the product #{product_id} (s/n): ").strip().lower())
        if confirmation == "s":
            cursor.execute("DELETE FROM products WHERE id =?", (product_id,))
            connection.commit()
            print("Product deleted.")
        else:
            print("Canceled operation.")
    except sql.Error as e:
        print(f"Error: {e}")
    finally:
        connection.close()


def menu():
    create_table()
    while True:
        print("Stock System")
        print("1. Register new product")
        print("2. List products")
        print("3. Update stock")
        print("4. Delete product")
        print("5. Exit")
        try:
            option = int(input("Choose an option: ").strip())
        except ValueError:
            print("Type only numbers.")
            continue
        
        match option:
            case 1:
                register_product()
            case 2:
                list_products()
            case 3:
                update_stock()
            case 4:
                delete_product()
            case 5:
                print("Bye!")
                break
            case _:
                print("Invalid option. Try again.")

menu() 