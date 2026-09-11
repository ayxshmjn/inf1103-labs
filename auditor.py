inventory = 0
failed_entries = 0
running_total = 0

while True: 
    user_input = input("Enter a stock quantity (or type 'quit' to stop): ").strip()

    if user_input.lower() == "quit":
        break
    elif user_input.isdigit():
        stock = int(user_input)
        inventory = inventory + stock
        print(f"Current Inventory: {inventory}")
        if inventory > 500:
            failed_entries += 1
            print("Error: Total Inventory exceeds 500 units")
            
            break
        
        running_total += stock
    else:
        failed_entries += 1
        continue
       
            
print(f"\n----- Daily Summary ----")
print(f"Total Units Processed: {inventory}")
print(f"Number of Failed/Rejected Entries: {failed_entries}")