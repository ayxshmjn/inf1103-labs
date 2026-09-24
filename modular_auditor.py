


def get_valid_input():
    """Handles user input and returns an integer quantity or 'quit'."""
    user_input = input("Enter a stock quantity (or type 'quit' to stop): ").strip()
    
    if user_input.lower() == "quit":
        return "quit"
    
    try:
        val = int(user_input)
        if val >= 0:
            return val
        else:
            return None  
    except ValueError:
        return None  


def process_delivery(current_total, new_value):
    
    return current_total + new_value


def calculate_tax(amount):
    
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    
    print("\n----- Daily Summary -----")
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


running_total = 0
deliveries_processed = 0
failed_entries = 0

while True:
    result = get_valid_input()

    if result == "quit":
        break  
    elif result is None:
        failed_entries += 1
        print("Invalid input! Skipping...")
    else:
        running_total = process_delivery(running_total, result)
        deliveries_processed += 1
        tax = calculate_tax(result)
        print(f"Added {result} units. Tax: {tax:.2f}. New Total: {running_total}")


generate_report(deliveries_processed, failed_entries)