def load_inventory():
    running_total = 0 #
    transaction_history = [] 
    orders = []
    reading_orders = False

    try:
        file = open("inventory.txt", "r")

        for line in file:
            line = line.strip()

            if line.startswith("New Total:"):
                running_total = int(line.replace("New Total:", "").strip())

            elif line.startswith("Transaction History:"):
                history_text = line.replace(
                    "Transaction History:", ""
                ).strip()

                history_text = history_text.strip("[]")

                if history_text != "":
                    amounts = history_text.split(",")

                    for amount in amounts:
                        transaction_history.append(int(amount.strip()))

            elif line == "Orders:":
                reading_orders = True

            elif reading_orders and line != "":
                orders.append(line)

        file.close()

    except FileNotFoundError:
        print("No inventory file found. Starting with empty inventory.")

    return running_total, transaction_history, orders


def save_inventory(running_total, transaction_history, orders):
    file = open("inventory.txt", "w")

    file.write("New Total: " + str(running_total) + "\n")
    file.write("Transaction History: " + str(transaction_history) + "\n\n")
    file.write("Orders:\n")

    for order in orders:
        file.write(order + "\n")

    file.close()


def display_orders(orders):
    print("\nCurrent Orders:\n")

    if len(orders) == 0:
        print("No orders found.")

    for order in orders:
        print(order)


def get_valid_input():
    user_input = input("Enter Quantity: ").strip()

    if user_input.lower() == "quit":
        return "quit"

    try:
        quantity = int(user_input)

        if quantity >= 0:
            return quantity

    except ValueError:
        return None

    return None


def process_delivery(current_total, new_value):
    return current_total + new_value


def generate_report(running_total, orders_processed, failed_entries):
    print("\n----- Daily Summary -----")
    print("Total Units in Inventory:", running_total)
    print("New Orders Processed:", orders_processed)
    print("Failed Entries:", failed_entries)


running_total, transaction_history, orders = load_inventory()

display_orders(orders)

orders_processed = 0
failed_entries = 0
next_order_id = 1001

if len(orders) > 0:
    last_order = orders[-1]
    last_order_parts = last_order.split(",")
    next_order_id = int(last_order_parts[0]) + 1

while True:
    product_name = input(
        "\nEnter Product Name (or type 'quit' to stop): "
    ).strip()

    if product_name.lower() == "quit":
        break

    if product_name == "":
        failed_entries += 1
        print("Product name cannot be empty.")
        continue

    if any(character.isdigit() for character in product_name):
        failed_entries += 1
        print("Product name cannot contain numbers.")
        continue

    quantity = get_valid_input()

    if quantity == "quit":
        break

    if quantity is None:
        failed_entries += 1
        print("Invalid quantity.")
        continue

    running_total = process_delivery(running_total, quantity)
    transaction_history.append(quantity)

    new_order = (
        str(next_order_id) + ", " +
        product_name + ", " +
        str(quantity)
    )

    orders.append(new_order)

    print("\nNew Order Added:")
    print(new_order)

    next_order_id += 1
    orders_processed += 1

save_inventory(running_total, transaction_history, orders)

print("\nOrder successfully saved to inventory.txt")

generate_report(running_total, orders_processed, failed_entries)