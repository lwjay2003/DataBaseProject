import signal
import sys
from database import PizzaDatabase
import datetime

doc = """
Welcome to Jay and stella's pizza, Use Following commands to operate:
- menu
  Prints available pizzas and side dishes.
- order item1 item2 ...
  Place a new order. Add items separated by a space.
  Use 'P' before pizza IDs and 'S' before side dish IDs.
  Example: order P1 P2 S1 S1
- cancel order_id1 order_id2 ...
  Cancel an existing order.
- status order_id1 order_id2 ...
  Check the status of orders.
- delivery
  Check all delivery persons' status.
- show my orders
  Display customer information and past orders.
- restaurant
  Display pizzas that have been ordered but not yet dispatched for delivery.
- report
  Generate monthly earnings report for the restaurant
- assign deliveries
  Assign pending deliveries to available delivery persons.
- reset
  Reset all orders in the system.
- help
  Show this message.
- quit
  Quit the app
"""

def parse_order(db, ids):
    pizzas = {}
    sidedishes = {}
    menu_items = db.get_menu_items()
    pizzas_dict = {f"P{pizza['id']}": pizza for pizza in menu_items['pizzas']}
    sidedishes_dict = {f"S{sd['id']}": sd for sd in menu_items['sidedishes']}

    for id in ids:
        if id.startswith('P') and id in pizzas_dict:
            if id in pizzas:
                pizzas[id] += 1
            else:
                pizzas[id] = 1
        elif id.startswith('S') and id in sidedishes_dict:
            if id in sidedishes:
                sidedishes[id] += 1
            else:
                sidedishes[id] = 1
        else:
            print(f"Invalid item ID '{id}'")
            return None, None
    if not pizzas:
        print("Order must contain at least one pizza.")
        return None, None

    print("Ordering:")
    for id, qty in pizzas.items():
        pizza = pizzas_dict[id]
        print(f"Pizza {pizza['name']} x {qty}")
    for id, qty in sidedishes.items():
        sd = sidedishes_dict[id]
        print(f"Side Dish {sd['name']} x {qty}")
    return pizzas, sidedishes


def setup_customer(db):
    while True:
        if input("Do you have a customer ID? (y/n) > ").strip().lower() == 'y':
            customer_id = input("Your customer ID > ").strip()
            customer = db.get_customer_info(customer_id)
            if customer:
                print(
                    f"Customer found: {customer['name']}, {customer['address']}, {customer['postcode']}, {customer['phone']}")
                return customer_id, customer  # Return the customer data as well
            else:
                print("ID does not exist. Please try again.")
        else:
            # Register a new customer
            print("Let's make an account for you!")
            name = input("Name > ").strip()
            gender = input("Gender (MALE/FEMALE) > ").strip().upper()
            birthday = input("Birthday (YYYY-MM-DD) > ").strip()
            address = input("Address > ").strip()
            postcode = input("Postcode > ").strip()
            phone = input("Phone number > ").strip()

            if not postcode[:4].isdigit():
                print("Invalid postcode. Please write postcode like 1234XX.")
            elif not db.exists('delivery_person', 'postcode', postcode):
                print(f"Cannot deliver to postal code {postcode}. Please try another address.")
            else:
                customer_id = db.create_customer(name, gender, birthday, address, postcode, phone)
                print(f"Registered successfully! Your customer ID is {customer_id}")
                # Fetch the customer data
                customer = db.get_customer_info(customer_id)
                return customer_id, customer  # Return the customer data as well



def cancel_order(db, order_id):
    db.cancel_order(order_id)


def check_coupon(db, customer_id, pizzas_ordered):
    """
    Automatically apply a 10% discount if the customer has accumulated 10 or more pizzas.
    Update the accumulation with the current order's pizzas.
    """
    # Get the customer's current accumulation
    accumulation = db.get_customer_accumulation(customer_id)
    print(f"Current accumulation: {accumulation}")

    # Add the number of pizzas ordered in the current order
    total_pizzas_ordered = sum(pizzas_ordered.values())
    print(f"Pizzas ordered in this order: {total_pizzas_ordered}")

    new_accumulation = accumulation + total_pizzas_ordered
    print(f"New accumulation (including this order): {new_accumulation}")

    # Check if the customer has earned a discount
    if new_accumulation >= 10:
        print("- You have ordered 10 or more pizzas! A 10% discount has been applied to your order.")

        # Apply the discount and reset the accumulation
        pizzas_to_reset = new_accumulation - 10
        db.reset_customer_accumulation(customer_id, pizzas_to_reset)
        return 0.9  # Apply 10% discount
    else:
        pizzas_needed = 10 - new_accumulation
        print(f"- You need {pizzas_needed} more pizza(s) to earn a 10% discount on your next order.")

    return 1.0  # No discount


def is_customer_birthday(customer):
    """
    Check if today is the customer's birthday.

    Args:
        customer (dict): Customer information dictionary.

    Returns:
        bool: True if today is the customer's birthday, False otherwise.
    """
    if 'birthday' not in customer or not customer['birthday']:
        return False

    try:
        birthday = customer['birthday']
        if isinstance(birthday, str):
            birthday = datetime.datetime.strptime(birthday, '%Y-%m-%d').date()
        today = datetime.date.today()
        return birthday.month == today.month and birthday.day == today.day
    except Exception as e:
        print(f"Error checking birthday: {e}")
        return False



def show_order(db, pizzas, sidedishes, discount, birthday_offer_applied=False):
    total_price = 0.0
    menu_items = db.get_menu_items()
    pizzas_dict = {f"P{pizza['id']}": pizza for pizza in menu_items['pizzas']}
    sidedishes_dict = {f"S{sd['id']}": sd for sd in menu_items['sidedishes']}

    print("Your order details:")

    # Process pizzas
    for id, qty in pizzas.items():
        pizza = pizzas_dict[id]
        price_per_item = pizza['price']
        total_item_price = price_per_item * qty

        # Check if birthday offer applies specifically to P1
        if birthday_offer_applied and id == "P1" and qty > 0:
            # Apply the offer only to pizza P1 and make it free
            qty_to_charge = qty - 1 if qty > 0 else 0
            total_item_price = price_per_item * qty_to_charge
            total_price += total_item_price
            print(f"- Pizza {pizza['name']} x {qty} (P1 free) @ €{price_per_item:.2f} each = €{total_item_price:.2f}")
        else:
            total_price += total_item_price
            print(f"- Pizza {pizza['name']} x {qty} @ €{price_per_item:.2f} each = €{total_item_price:.2f}")

    # Process side dishes
    for id, qty in sidedishes.items():
        sd = sidedishes_dict[id]
        price_per_item = sd['price']
        total_item_price = price_per_item * qty

        # Check if birthday offer applies specifically to S1
        if birthday_offer_applied and id == "S1" and qty > 0:
            # Apply the offer only to side dish S1 and make it free
            qty_to_charge = qty - 1 if qty > 0 else 0
            total_item_price = price_per_item * qty_to_charge
            total_price += total_item_price
            print(f"- Side Dish {sd['name']} x {qty} (S1 free) @ €{price_per_item:.2f} each = €{total_item_price:.2f}")
        else:
            total_price += total_item_price
            print(f"- Side Dish {sd['name']} x {qty} @ €{price_per_item:.2f} each = €{total_item_price:.2f}")

    total_price_discounted = total_price * discount
    print(f"- Total price: €{total_price_discounted:.2f} (original price: €{total_price:.2f})")



def get_existing_customer_id(db):
    while True:
        customer_id = input("Please enter your customer ID > ").strip()
        customer = db.get_customer_info(customer_id)
        if customer:
            print(
                f"Customer found: {customer['name']}, {customer['address']}, {customer['postcode']}, {customer['phone']}")
            return customer_id
        else:
            print("Customer ID does not exist. Please try again.")


# Signal handler for catching Ctrl+C interrupts
def signal_handler(sig, frame):
    print("\nApplication interrupted. Exiting gracefully...")
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    db = PizzaDatabase()

    try:


        while True:
            input_str = input("Enter command (\"help\" for available commands)\n > ").strip()
            if not input_str:
                continue
            input_parts = input_str.strip().split()
            command = input_parts[0].lower()
            args = input_parts[1:]

            if command == "menu":
                menu_items = db.get_menu_items()
                print("- Pizzas:")
                # Prepare header
                print("{:<5} {:<25} {:<10} {}".format("ID", "Name", "Price", "Ingredients"))
                print("-" * 80)

                # Loop through each pizza and append the label (vegetarian/vegan)
                for pizza in menu_items['pizzas']:
                    # Get the pizza status (vegetarian or vegan)
                    pizza_status = db.get_pizza_status(pizza['id'])
                    status_label = ""

                    # Set the appropriate label based on the pizza's status
                    if pizza_status["vegan"]:
                        status_label = "(Vegan)"
                    elif pizza_status["vegetarian"]:
                        status_label = "(Vegetarian)"

                    # Prepare the ingredients string
                    ingredients = pizza['ingredient_names']

                    # Print pizza details with the status label
                    print("{:<5} {:<25} €{:<9.2f} {}".format(f"P{pizza['id']}", f"{pizza['name']} {status_label}",
                                                             pizza['price'], ingredients))

                print("\n- Side Dishes:")
                print("{:<5} {:<25} {:<10}".format("ID", "Name", "Price"))
                print("-" * 40)
                for sd in menu_items['sidedishes']:
                    print("{:<5} {:<25} €{:<9.2f}".format(f"S{sd['id']}", sd['name'], sd['price']))


            elif command == "order":
                if not args:
                    print("Please specify items to order.")
                    print("Example: order P1 P2 S1 S2")
                    continue
                pizzas, sidedishes = parse_order(db, args)
                if not pizzas:
                    continue
                customer_id, customer = setup_customer(db)
                if not customer_id:
                    continue

                # Check if today is the customer's birthday
                birthday_offer_applied = False
                if is_customer_birthday(customer):
                    print("Happy Birthday! You are eligible for a free pizza and a free drink!")
                    birthday_offer_applied = True

                    # Apply the offer by adding a free pizza and drink
                    free_pizza_id = 'P1'  # Default free pizza ID
                    if free_pizza_id in pizzas:
                        pizzas[free_pizza_id] += 1
                    else:
                        pizzas[free_pizza_id] = 1

                    free_drink_id = 'S1'  # Default free drink ID
                    if free_drink_id in sidedishes:
                        sidedishes[free_drink_id] += 1
                    else:
                        sidedishes[free_drink_id] = 1

                # Check for coupon (pass the pizzas for current order to check_coupon)
                discount = check_coupon(db, customer_id, pizzas)

                # Place order
                pizzas_numeric = {id[1:]: qty for id, qty in pizzas.items()}
                sidedishes_numeric = {id[1:]: qty for id, qty in sidedishes.items()}
                order_id = db.place_order(customer_id, pizzas_numeric, sidedishes_numeric)
                if order_id:
                    print("+-----------------------------------------------------------+")
                    print(f"- Your order id is: {order_id}")
                    print("- You can cancel your order within 5 minutes using your order id.\n")
                    show_order(db, pizzas, sidedishes, discount, birthday_offer_applied)
                    print("+-----------------------------------------------------------+")
                    estimated_delivery_time = datetime.datetime.now() + datetime.timedelta(minutes=30)
                    print(f"- Your estimated delivery time: {estimated_delivery_time.strftime('%Y-%m-%d %H:%M')}")
                else:
                    print("Error placing order.")

            elif command == "cancel":
                for order_id in args:
                    cancel_order(db, order_id)
            elif command == "show":
                if len(args) >= 2 and args[0] == "my" and args[1] == "orders":
                    customer_id = get_existing_customer_id(db)
                    if customer_id:
                        pizzas = db.get_customer_pizza_orders(customer_id)
                        if pizzas:
                            print("You have ordered the following pizzas:")
                            total_pizzas = 0
                            for pizza_id, pizza_name, total_quantity in pizzas:
                                print(f"- {pizza_name} x {total_quantity}")
                                total_pizzas += total_quantity
                            print(f"Total number of pizzas ordered: {total_pizzas}")
                        else:
                            print("You have not ordered any pizzas yet.")
                    else:
                        print("Unable to retrieve customer information.")

            elif command == "restaurant":

                    orders_in_oven = db.get_pizzas_still_in_oven()
                    if orders_in_oven:
                        print("Pizzas still in the oven (not yet dispatched for delivery):")
                        print("{:<10} {:<20} {:<10} {:<20}".format("Order ID", "Pizza Name", "Quantity", "Order Time"))
                        print("-" * 70)
                        for order in orders_in_oven:
                            print("{:<10} {:<20} {:<10} {:<20}".format(order['order_id'], order['pizza_name'],
                                                                       order['quantity'],
                                                                       order['order_time'].strftime('%Y-%m-%d %H:%M')))
                    else:
                        print("There are no pizzas currently in the oven.")
            elif command == "status":
                for order_id in args:
                    status = db.get_order_status([order_id])
                    print(status)
            elif command == "delivery":
                delivery_persons = db.get_delivery_person_status()
                if delivery_persons:
                    print("{:<5} {:<20} {:<10} {}".format("ID", "Name", "Postcode", "Next Available Time"))
                    print("-" * 60)
                    for dp in delivery_persons:
                        time_str = dp['time'].strftime('%Y-%m-%d %H:%M') if dp['time'] else 'Available Now'
                        print("{:<5} {:<20} {:<10} {}".format(dp['id'], dp['name'], dp['postcode'], time_str))
                else:
                    print("No delivery person information available.")


            elif command == "assign" and len(args) >= 1 and args[0] == "deliveries":
                if db.assign_delivery_person2():
                    print("Pending deliveries have been assigned.")
                else:
                    print("Failed to assign deliveries.")
            elif command.lower() == "report":
                filters = {}
                # Prompt for filters
                print("Generating Monthly Earnings Report.")
                use_filters = input("Do you want to apply any filters? (y/n) > ").strip().lower()
                if use_filters == 'y':
                    # Filter by postcode
                    filter_postcode = input("Filter by postcode? (leave blank to skip) > ").strip()
                    if filter_postcode:
                        filters['postcode'] = filter_postcode

                    # Filter by customer gender
                    filter_gender = input("Filter by gender? (MALE/FEMALE, leave blank to skip) > ").strip().upper()
                    if filter_gender in ('MALE', 'FEMALE'):
                        filters['gender'] = filter_gender

                    # Filter by age range
                    filter_age = input("Filter by age range? (e.g., 18-25, leave blank to skip) > ").strip()
                    if filter_age:
                        try:
                            age_min, age_max = map(int, filter_age.split('-'))
                            filters['age_min'] = age_min
                            filters['age_max'] = age_max
                        except ValueError:
                            print("Invalid age range format. Skipping age filter.")

                report = db.generate_monthly_earnings_report(filters)
                if report:
                    print("\nMonthly Earnings Report:")
                    print(f"Total Earnings: €{report['total_earnings']:.2f}")
                    print(f"Number of Orders: {report['order_count']}")
                    print(f"Number of Pizzas Sold: {report['pizza_count']}")
                    print(f"Number of Side Dishes Sold: {report['sidedish_count']}")
                else:
                    print("No data available for the given filters.")

            #reset the table of orders in database
            elif command == "reset":
                confirm = input(
                    "Are you sure you want to reset all orders? This action cannot be undone. (y/n) > ").strip().lower()
                if confirm == 'y':
                    db.reset_orders()
                else:
                    print("Reset operation cancelled.")
            elif command == "help":
                print(doc)
            elif command == "quit":
                break
            else:
                print(f"Unknown command '{command}'")


    # Catching the KeyboardInterrupt exception when Ctrl+C is pressed
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
