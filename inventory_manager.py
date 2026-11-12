import json
import os
from abc import ABC, abstractmethod


class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self.supplier_id: str = supplier_id
        self.name: str = name
        self.contact_email: str = contact_email

    def display_information(self) -> None:
        print(
            f"Supplier ID: {self.supplier_id} | Name: {self.name} | "
            f"Email: {self.contact_email}"
        )

    def to_dict(self) -> dict:
        return {
            "supplier_id": self.supplier_id,
            "name": self.name,
            "contact_email": self.contact_email,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Supplier":
        return cls(
            supplier_id=data.get("supplier_id", "Unknown"),
            name=data.get("name", "Unknown Supplier"),
            contact_email=data.get("contact_email", "N/A"),
        )


class Product(ABC):
    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
    ):
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.supplier: Supplier = supplier

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    def update_stock(self, new_stock: int) -> bool:
        if new_stock >= 0:
            self.__stock = new_stock
            return True
        return False

    def display_information(self) -> None:
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )
        self.supplier.display_information()

    def to_dict(self) -> dict:
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.supplier.to_dict(),
        }


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass


class PhysicalProduct(Product, CanBeShipped):
    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
        weight: float,
    ):
        super().__init__(product_id, name, price, stock, supplier)
        self.weight: float = weight

    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self.weight} kg")
        print(f"Fulfilment: {self.get_fulfilment_info()}")
        print(f"Est. Shipping Cost: ${self.calculate_shipping_cost():.2f}")

    def get_fulfilment_info(self) -> str:
        return "Product requires physical shipping"

    def calculate_shipping_cost(self) -> float:
        return max(5.00, self.weight * 2.00)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["product_type"] = "physical"
        data["weight"] = self.weight
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "PhysicalProduct":
        supplier_data = data.get("supplier", {})
        supplier = Supplier.from_dict(supplier_data)
        return cls(
            product_id=data["id"],
            name=data["name"],
            price=float(data["price"]),
            stock=int(data["stock"]),
            supplier=supplier,
            weight=float(data.get("weight", 0.0)),
        )


class DigitalProduct(Product):
    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
        download_size: float,
    ):
        super().__init__(product_id, name, price, stock, supplier)
        self.download_size: float = download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"Download Size: {self.download_size} MB")
        print(f"Fulfilment: {self.get_fulfilment_info()}")

    def get_fulfilment_info(self) -> str:
        return "Product is delivered digitally"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["product_type"] = "digital"
        data["download_size"] = self.download_size
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "DigitalProduct":
        supplier_data = data.get("supplier", {})
        supplier = Supplier.from_dict(supplier_data)
        return cls(
            product_id=data["id"],
            name=data["name"],
            price=float(data["price"]),
            stock=int(data["stock"]),
            supplier=supplier,
            download_size=float(data.get("download_size", 0.0)),
        )


class Inventory:
    def __init__(self):
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self.__products.append(product)

    def remove_product(self, product_id: str) -> bool:
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
            return True
        return False

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.product_id == product_id:
                return product
        return None


    def display_all(self) -> None:
        print("\nCurrent Inventory")
        print("========================================")
        if not self.__products:
            print("No products found in inventory.")
            print("========================================")
            return

        for product in self.__products:
            product.display_information()
            print("-" * 40)
        print("========================================")

    def get_all_products(self) -> list[Product]:
        return self.__products


class OrderLine:
    def __init__(self, product: Product, quantity: int):
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity

    def display_information(self) -> None:
        print(
            f"Product: {self.product.name} (ID: {self.product.product_id}) | "
            f"Unit Price: ${self.product.price:.2f} | Qty: {self.quantity} | "
            f"Subtotal: ${self.calculate_subtotal():.2f}"
        )


class Order:
    def __init__(self, order_id: str):
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        for line in self.order_lines:
            if line.product.product_id == product_id:
                self.order_lines.remove(line)
                return True
        return False

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def display_information(self) -> None:
        print(f"\nOrder ID: {self.order_id}")
        print("----------------------------------------")
        if not self.order_lines:
            print("No items present in this order.")
        else:
            for line in self.order_lines:
                line.display_information()
        print("----------------------------------------")
        print(f"Order Total: ${self.calculate_total():.2f}")


def load_inventory() -> Inventory:
    inventory = Inventory()
    if os.path.exists("inventory.json"):
        try:
            with open("inventory.json", "r") as file:
                data = json.load(file)
                for item in data:
                    p_type = item.get("product_type", "physical")
                    if p_type == "digital":
                        product = DigitalProduct.from_dict(item)
                    else:
                        product = PhysicalProduct.from_dict(item)
                    inventory.add_product(product)
                print("Inventory loaded successfully.")
                return inventory
        except (json.JSONDecodeError, KeyError, ValueError):
            print("Error reading inventory file. Starting with an empty inventory.")
            return Inventory()
    print("inventory.json not found. Starting with an empty inventory.")
    return inventory


def save_inventory(inventory: Inventory) -> None:
    data = [product.to_dict() for product in inventory.get_all_products()]
    with open("inventory.json", "w") as file:
        json.dump(data, file, indent=3)


def add_product_cli(inventory: Inventory) -> None:
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    p_type = input("Select product type (1 or 2): ").strip()

    if p_type not in ["1", "2"]:
        print("Invalid choice. Operation cancelled.")
        return

    product_id = input("Product ID: ").strip()

    if inventory.find_product(product_id) is not None:
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

    supplier_id = input("Supplier ID: ").strip()
    supplier_name = input("Supplier Name: ").strip()
    contact_email = input("Supplier Contact Email: ").strip()
    supplier = Supplier(supplier_id, supplier_name, contact_email)

    if p_type == "1":
        try:
            weight = float(input("Weight (kg): ").strip())
            if weight < 0:
                print("Weight cannot be negative.")
                return
            new_product = PhysicalProduct(
                product_id, name, price, stock, supplier, weight
            )
        except ValueError:
            print("Invalid weight input.")
            return
    else:
        try:
            download_size = float(input("Download Size (MB): ").strip())
            if download_size < 0:
                print("Download size cannot be negative.")
                return
            new_product = DigitalProduct(
                product_id, name, price, stock, supplier, download_size
            )
        except ValueError:
            print("Invalid download size input.")
            return

    inventory.add_product(new_product)
    print("\nProduct added successfully!")


def update_stock_cli(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()

    product = inventory.find_product(product_id)
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


def search_product_cli(inventory: Inventory) -> None:
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()

    product = inventory.find_product(product_id)
    if product:
        print("Product Found")
        print("========================================")
        product.display_information()
        print("========================================")
    else:
        print("Product not found.")


def remove_product_cli(inventory: Inventory) -> None:
    print("\nRemove Product")
    product_id = input("Enter Product ID to remove: ").strip()

    if inventory.remove_product(product_id):
        print(f"Product ID {product_id} removed successfully!")
    else:
        print(f"Product ID {product_id} not found.")


def create_order_cli(inventory: Inventory) -> None:
    print("\nCreate Customer Order")
    order_id = input("Enter Order ID: ").strip()
    if not order_id:
        print("Order ID cannot be empty.")
        return

    order = Order(order_id)

    while True:
        product_id = input("Enter Product ID to add (or 'done' to finish): ").strip()
        if product_id.lower() == "done":
            break

        product = inventory.find_product(product_id)
        if not product:
            print(f"Product ID {product_id} not found in inventory.")
            continue

        try:
            quantity = int(input("Enter Quantity: ").strip())
            if quantity <= 0:
                print("Quantity must be greater than zero.")
                continue
            order.add_order_line(product, quantity)
            print(f"Added {quantity} x {product.name} to order.")
        except ValueError:
            print("Invalid quantity input.")

    order.display_information()


def main() -> None:
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
        print("5. Remove Product")
        print("6. Create Order")
        print("7. Save Inventory")
        print("8. Exit")
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
            remove_product_cli(inventory)
        elif choice == "6":
            create_order_cli(inventory)
        elif choice == "7":
            print("\nSaving inventory...")
            save_inventory(inventory)
            print("Inventory saved successfully to inventory.json.")
        elif choice == "8":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()