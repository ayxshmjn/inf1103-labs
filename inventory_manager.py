import json
import os


def load_inventory():
    
    if os.path.exists("inventory.json"):
        try:
            with open("inventory.json", "r") as file:
                print("inventory.json found.")
                print("Inventory loaded successfully.")
                return json.load(file)
        except json.JSONDecodeError:
            print("Error reading inventory file. Starting with an empty inventory.")
            return []
    print("inventory.json not found. Starting with an empty inventory.")
    return []


def save_inventory(inventory):
    
    with open("inventory.json", "w") as file:
        json.dump(inventory, file, indent=4)


def display_all(inventory):
    
    print("\nCurrent Inventory")
    print("-" * 48)
    if not inventory:
        print("No products found in inventory.")
        print("-" * 48)
        return

    for item in inventory:
        print(f"ID: {item['id']} | Name: {item['name']} | Price: ${item['price']:.2f} | Stock: {item['stock']}")
    print("-" * 48)


def add_product(inventory):
    
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    
    # Check if product ID already exists
    for item in inventory:
        if item["id"] == product_id:
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

    inventory.append({
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock
    })
    print("\nProduct added successfully!")


def update_stock(inventory):
    
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()

    found_item = None
    for item in inventory:
        if item["id"] == product_id:
            found_item = item
            break

    if not found_item:
        print(f"Product ID {product_id} not found.")
        return

    print(f"Product Found:")
    print(f"Name: {found_item['name']}")
    print(f"Current Stock: {found_item['stock']}")

    try:
        new_stock = int(input("New Stock Quantity: ").strip())
        if new_stock < 0:
            print("Stock cannot be negative.")
            return
        found_item["stock"] = new_stock
        print("Stock updated successfully!")
    except ValueError:
        print("Invalid stock quantity input.")


def search_product(inventory):
   
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()

    for item in inventory:
        if item["id"] == product_id:
            print("Product Found")
            print("-" * 48)
            print(f"ID: {item['id']}")
            print(f"Name: {item['name']}")
            print(f"Price: ${item['price']:.2f}")
            print(f"Stock: {item['stock']}")
            print("-" * 48)
            return

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
            display_all(inventory)
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
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



main()