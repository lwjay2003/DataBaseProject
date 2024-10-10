from database import PizzaDatabase
import datetime

doc = """
Available commands:
- menu
  Prints available pizzas and side dishes.
- order item1 item2 ...
  Place a new order. Add items separated by a space.
- cancel order_id1 order_id2 ...
  Cancel an existing order.
- status order_id1 order_id2 ...
  Check the status of orders.
- delivery
  Check all delivery persons' status.
- help
  Show this message.
- quit
  Quit the app.
"""

def parse_order(db, ids):
    pizzas = {}
    sidedishes = {}
    menu_items = db.get_menu_items()
    pizzas_dict = {str(pizza['id']): pizza for pizza in menu_items['pizzas']}
    sidedishes_dict = {str(sd['id']): sd for sd in menu_items['sidedishes']}

    for id in ids:
        if id in pizzas_dict:
            if id in pizzas:
                pizzas[id] += 1
            else:
                pizzas[id] = 1
        elif id in sidedishes_dict:
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
        choice = input("Do you have an account? (y/n) > ").strip().lower()
        if choice == 'y':
            username = input("Username > ").strip()
            password = input("Password > ").strip()
            customer_id = db.login(username, password)
            if customer_id:
                customer_info = db.get_customer_info(customer_id)
                if customer_info:
                    print(f"- Your information: name: {customer_info['name']}, address: {customer_info['address']}, postcode: {customer_info['postcode']}, phone number: {customer_info['phone']}.")
                    return customer_id
                else:
                    print("Customer information not found.")
            else:
                print("Invalid username or password.")
        else:
            print("Account creation is not supported at this time. Please contact support.")
            return None

def cancel_order(db, order_id):
    db.cancel_order(order_id)

def check_coupon(db, customer_id):
    if db.has_valid_coupon(customer_id):
        use_coupon = input("You have a valid coupon. Do you want to use it? (y/n) > ").strip().lower()
        if use_coupon == 'y':
            coupon_info = db.has_valid_coupon(customer_id)
            if db.redeem_coupon(coupon_info['coupon_id']):
                print("- Coupon applied for a 10% discount.")
                return 0.9
    else:
        if db.check_coupon(customer_id):
            print("- You have accumulated enough points for a 10% discount coupon. It has been applied to your account.")
    return 1.0

def show_order(db, pizzas, sidedishes, discount):
    total_price = 0.0
    menu_items = db.get_menu_items()
    pizzas_dict = {str(pizza['id']): pizza for pizza in menu_items['pizzas']}
    sidedishes_dict = {str(sd['id']): sd for sd in menu_items['sidedishes']}

    print("Your order details:")
    for id, qty in pizzas.items():
        pizza = pizzas_dict[id]
        price = pizza['price'] * qty
        total_price += price
        print(f"- Pizza {pizza['name']} x {qty} @ €{pizza['price']:.2f} each = €{price:.2f}")

    for id, qty in sidedishes.items():
        sd = sidedishes_dict[id]
        price = sd['price'] * qty
        total_price += price
        print(f"- Side Dish {sd['name']} x {qty} @ €{sd['price']:.2f} each = €{price:.2f}")

    total_price_discounted = total_price * discount
    print(f"- Total price: €{total_price_discounted:.2f} (original price: €{total_price:.2f})")

if __name__ == "__main__":
    db = PizzaDatabase()

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
            for pizza in menu_items['pizzas']:
                print(f"  ID: {pizza['id']}, Name: {pizza['name']}, Price: €{pizza['price']:.2f}, Ingredients: {pizza['ingredient_names']}")
            print("- Side Dishes:")
            for sd in menu_items['sidedishes']:
                print(f"  ID: {sd['id']}, Name: {sd['name']}, Price: €{sd['price']:.2f}")
        elif command == "order":
            if not args:
                print("Please specify items to order.")
                continue
            pizzas, sidedishes = parse_order(db, args)
            if not pizzas:
                continue
            customer_id = setup_customer(db)
            if not customer_id:
                continue
            # Check for coupon
            discount = check_coupon(db, customer_id)
            # Place order
            order_id = db.place_order(customer_id, pizzas, sidedishes)
            if order_id:
                print("+-----------------------------------------------------------+")
                print(f"- Your order id is: {order_id}")
                print("- You can cancel your order within 5 minutes using your order id.\n")
                show_order(db, pizzas, sidedishes, discount)
                print("+-----------------------------------------------------------+")
                # Assign delivery person
                if db.assign_delivery_person(order_id):
                    print("- Your order has been assigned to a delivery person.")
                else:
                    print("- We couldn't assign a delivery person at this time.")
            else:
                print("Error placing order.")
        elif command == "cancel":
            for order_id in args:
                cancel_order(db, order_id)
        elif command == "status":
            for order_id in args:
                status = db.get_order_status([order_id])
                print(status)
        elif command == "delivery":
            delivery_persons = db.get_delivery_person_status()
            if delivery_persons:
                for dp in delivery_persons:
                    print(f"ID: {dp['id']}, Name: {dp['name']}, Postcode: {dp['postcode']}, Next Available Time: {dp['time']}")
            else:
                print("No delivery person information available.")
        elif command == "help":
            print(doc)
        elif command == "quit":
            break
        else:
            print(f"Unknown command '{command}'")
