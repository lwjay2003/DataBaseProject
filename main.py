from database import PizzaDatabase
import datetime

doc = """
available commands:
- menu
  Prints available pizzas, drinks, and desserts
- order item1 item2 ...
  Place a new order with id (eg. p1/d1). Add items split by a single space.
- cancel order_id1 order_id2 ...
  Cancel an existing order.
- status order_id1 order_id2 ...
  Check the status of orders.
- delivery
  Check all deliverymen's status.
- reset
  Reset the database to the initial state.
- help
  Show this message.
- quit
  Quit the app.
"""


# Helper function to parse orders
def parse_order(db, ids):
    pizzas = []
    side_dishes = []

    for id in ids:
        if id.startswith('p') and db.get_pizza(id[1:]):
            pizzas.append(id[1:])
        elif id.startswith('d') and db.get_side_dish(id[1:]):
            side_dishes.append(id[1:])
        else:
            print(f"Invalid id '{id}'")
            return [], []

    if not pizzas:
        print("You must order at least one pizza.")
        return [], []

    print("Ordering:")
    for pizza_id in pizzas:
        pizza = db.get_pizza(pizza_id)
        print(
            f"- Pizza: {pizza['name']} (Ingredients: {', '.join([db.get_ingredient(i)['name'] for i in pizza['ingredients']])})")

    for side_dish_id in side_dishes:
        side_dish = db.get_side_dish(side_dish_id)
        print(f"- Side Dish: {side_dish['name']}")

    return pizzas, side_dishes


# Setup a new customer or validate an existing one
def setup_customer(db):
    while True:
        if input("Do you have a customer ID? (y/n) > ").strip().lower() == 'y':
            customer_id = input("Your customer ID > ").strip()
            customer = db.get_customer_info(customer_id)
            if customer:
                print(
                    f"Customer found: {customer['name']}, {customer['address']}, {customer['postcode']}, {customer['phone']}")
                return customer_id
            else:
                print("ID does not exist. Please try again.")
        else:
            # Register a new customer
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
                return customer_id


# Cancel an order
def cancel_order(db, order_id):
    if db.id_exists("order_info", order_id):
        if datetime.datetime.now() + datetime.timedelta(minutes=-5) > db.get_order_time(order_id):
            print(f"Cannot cancel order {order_id}, more than 5 minutes have passed.")
        else:
            db.cancel_order(order_id)
            print(f"Order {order_id} cancelled successfully.")
    else:
        print(f"Order {order_id} doesn't exist.")


# Check coupon
def check_coupon(db):
    coupon = input("Enter your coupon code (or 'n' if none) > ").strip().lower()
    if coupon == 'n':
        return 1.0
    elif db.check_coupon(coupon):
        db.redeem_coupon(coupon)
        return 0.9
    else:
        print("Invalid coupon. No discount applied.")
        return 1.0


# Main application loop
if __name__ == "__main__":
    db = PizzaDatabase()

    while True:
        input_str = input("Enter command (\"help\" for available commands)\n > ").strip().lower()
        command = input_str.split(" ", 1)[0]
        args = input_str.split(" ")[1:] if len(input_str.split(" ", 1)) > 1 else []

        if command == "menu":
            print("- Pizzas:")

            for pizza_id in range(1, 12):  # Assuming you have pizza IDs from 1 to 11
                pizza = db.get_pizza(pizza_id)

                # Fetch the ingredients and their prices
                ingredient_details = []
                total_ingredient_cost = 0

                for ingredient_id in pizza['ingredients']:
                    ingredient = db.get_ingredient(ingredient_id)
                    ingredient_details.append(f"{ingredient['name']} (€{ingredient['price']})")
                    total_ingredient_cost += ingredient['price']

                # Calculate the total price with profit margin and tax
                total_price_with_profit = total_ingredient_cost * 1.4
                total_price_with_tax = total_price_with_profit * 1.09

                # Fetch the vegetarian/vegan status
                status = db.get_pizza_status(pizza_id)

                # Determine the status label
                status_label = "(VEGAN)" if status["vegan"] else "(VEGETARIAN)" if status["vegetarian"] else ""

                # Display pizza with its ID and calculated price, including vegetarian/vegan status
                print(f"- p{pizza_id}: {pizza['name']} {status_label}")
                # Print ingredients and their prices in one line
                ingredients_line = ", ".join(ingredient_details)
                print(f"  Ingredients: {ingredients_line}")

                print(f"    Total price (including 9% tax): €{total_price_with_tax:.2f}\n")

            print("- Side Dishes:")

            for side_dish_id in range(1, 6):  # Assuming you have side dish IDs from 1 to 5
                side_dish = db.get_side_dish(side_dish_id)

                # Display side dish with its ID
                print(f"  d{side_dish_id} - {side_dish['name']} (Price: €{side_dish['price']})")


        elif command == "order":
            pizzas, side_dishes = parse_order(db, args)
            if not pizzas:
                continue

            customer_id = setup_customer(db)
            order_id = db.place_order(customer_id, pizzas, side_dishes)
            discount = check_coupon(db)

            print("+-----------------------------------------------------------+")
            print(f"- Your order ID is: {order_id}")
            print("- You can cancel your order within 5 minutes.")
            total_price = db.print_order(pizzas, side_dishes)
            print(f"- Total price: €{total_price * discount:.2f} (with discount: {discount * 100}%)")
            print("+-----------------------------------------------------------+")

            postcode = db.get_customer_info(customer_id)['postcode'][:4]
            delivery_time = db.assign_delivery_person(order_id)

            if not delivery_time:
                print(f"Cannot deliver to postal code {postcode}. Please try another address.")
                db.cancel_order(order_id)
            else:
                print(f"Your order will arrive around {delivery_time}")

        elif command == "cancel":
            for order in args:
                cancel_order(db, order)

        elif command == "reset":
            print("Resetting the database...")
            db.reset()
            print("Done.")

        elif command == "delivery":
            db.print_delivery_persons()

        elif command == "status":
            db.get_order_status(args)

        elif command == "help":
            print(doc)

        elif command == "quit":
            exit(0)

        else:
            print(f"Unknown command: {command}")
