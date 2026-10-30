import json
import os


class Product:
    

    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    
    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock

    def update_stock(self, new_stock):
        if new_stock >= 0:
            self.__stock = new_stock
            return True
        return False

    def display_information(self):
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )

    def to_dict(self):
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            product_id=data["id"],
            name=data["name"],
            price=float(data["price"]),
            stock=int(data["stock"]),
        )


class Inventory:
    

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        self.__products.append(product)

    def search_product(self, product_id):
        for product in self.__products:
            if product.product_id == product_id:
                return product
        return None

    def display_all(self):
        print("\nCurrent Inventory")
        print("========================================")
        if not self.__products:
            print("No products found in inventory.")
            print("========================================")
            return

        for product in self.__products:
            product.display_information()
        print("-" * 50)

    def get_all_products(self):
        return self.__products


def load_inventory():
    inventory = Inventory()
    if os.path.exists("inventory.json"):
        try:
            with open("inventory.json", "r") as file:
                data = json.load(file)
                print("inventory.json found.")
                print("Inventory loaded successfully.")
                for item in data:
                    product = Product.from_dict(item)
                    inventory.add_product(product)
                return inventory
        except (json.JSONDecodeError, KeyError, ValueError):
            print("Error reading inventory file. Starting with an empty inventory.")
            return Inventory()
    print("inventory.json not found. Starting with an empty inventory.")
    return inventory


def save_inventory(inventory):
    data = [product.to_dict() for product in inventory.get_all_products()]
    with open("inventory.json", "w") as file:
        json.dump(data, file, indent=3)


def add_product_cli(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()

    if inventory.search_product(product_id) is not None:
        print("Product ID already exists!")
        return

    name = input("Product Name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return

    try:
        price = float(input("Price: ").strip())
        if price < 0:
            print("Price cannot be negative.")
            return
    except ValueError:
        print("Invalid price input.")
        return

    try:
        stock = int(input("Stock Quantity: ").strip())
        if stock < 0:
            print("Stock quantity cannot be negative.")
            return
    except ValueError:
        print("Invalid stock quantity input.")
        return

    new_product = Product(product_id, name, price, stock)
    inventory.add_product(new_product)
    print("\nProduct added successfully!")


def update_stock_cli(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()

    product = inventory.search_product(product_id)
    if not product:
        print(f"Product ID {product_id} not found.")
        return

    print("Product Found:")
    print(f"Name: {product.name}")
    print(f"Current Stock: {product.stock}")

    try:
        new_stock = int(input("New Stock Quantity: ").strip())
        if new_stock < 0:
            print("Stock cannot be negative.")
            return
        product.update_stock(new_stock)
        print("Stock updated successfully!")
    except ValueError:
        print("Invalid stock quantity input.")


def search_product_cli(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()

    product = inventory.search_product(product_id)
    if product:
        print("Product Found")
        print("========================================")
        product.display_information()
        print("========================================")
    else:
        print("Product not found.")


def main():
    print("========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================")

    inventory = load_inventory()

    while True:
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("----------------------------")

        choice = input("Enter option: ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product_cli(inventory)
        elif choice == "3":
            update_stock_cli(inventory)
        elif choice == "4":
            search_product_cli(inventory)
        elif choice == "5":
            print("\nSaving inventory...")
            save_inventory(inventory)
            print("Inventory saved successfully to inventory.json.")
        elif choice == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()