from database import PizzaDatabase

"""Please comment out other methods properly and double check with the database 
   when you want to test a single functionality"""

db = PizzaDatabase()

"""Testing Get Pizza Details"""
# Call the get_pizza method
pizza_info = db.get_pizza(5)

# Check if pizza_info is correct
if pizza_info:
    print(f"Pizza Name: {pizza_info['name']}")
    print("Ingredients:")
    for ingredient_id in pizza_info['ingredients']:
        db.cursor.execute("SELECT name FROM ingredient WHERE ingredient_id = %s;", (ingredient_id,))
        ingredient_name = db.cursor.fetchone()[0]
        print(f"- {ingredient_name}")
else:
    print("No such pizza found.")


"""Testing Get Ingredient Details"""
ingredient_id = 1
ingredient_info = db.get_ingredient(ingredient_id)

if ingredient_info:
    print(f"Ingredient Name: {ingredient_info['name']}")
    print(f"Category: {ingredient_info['category']}")
    print(f"Price: €{ingredient_info['price']:.2f}")
else:
    print(f"No ingredient found with id: {ingredient_id}")


"""Testing Get Side Dish Details"""

sidedish_id = 9
side_dish_info = db.get_side_dish(sidedish_id)

if side_dish_info:
    print(f"Side Dish Name: {side_dish_info['name']}")
    print(f"Price: €{side_dish_info['price']:.2f}")
else:
    print(f"No side dish found with id: {sidedish_id}")


"""Testing Login Functionality"""
customer_id = db.login("evi", "password2")
if customer_id:
    print(f"Login successful for customer_id: {customer_id}")
else:
    print("Login failed.")

"""Test Fetching Customer Info"""
customer_info = db.get_customer_info(1)
if customer_info:
    print("Customer Info:", customer_info)
else:
    print("No such customer found.")

"""Test Placing an Order"""
pizzas = [5]  # Example pizza IDs
side_dishes = [2]  # Example side dish ID
order_id = db.place_order(2, pizzas, side_dishes)
if order_id:
    print(f"Order placed successfully with order_id: {order_id}")
else:
    print("Failed to place order.")

"""Test Canceling an Order"""
db.cancel_order(12)
db.cancel_order(13)



# Test for get_order_info
order_id = 4
order_info = db.get_order_info(order_id)

if order_info:
    print("Order Information:")
    print(f"Order ID: {order_info['order_id']}")
    print(f"Customer Name: {order_info['customer_name']}")
    print(f"Order Time: {order_info['time']}")
    print(f"Delivery Address: {order_info['address']}")
else:
    print(f"No order found with order_id: {order_id}")


# Test for get_menu_items

"""Testing Get Menu Items"""
# Insert test pizzas and side dishes
db.cursor.execute("INSERT INTO pizza (name, price) VALUES ('Pepperoni', 10.0), ('Margherita', 8.0);")
db.cursor.execute("INSERT INTO sidedish (name, price) VALUES ('Garlic Bread', 3.5), ('Caesar Salad', 4.0);")
db.conn.commit()

menu_items = db.get_menu_items()
if menu_items:
    print("Menu Items:")
    print("Pizzas:")
    for pizza in menu_items["pizzas"]:
        print(pizza)
    print("Side Dishes:")
    for sidedish in menu_items["sidedishes"]:
        print(sidedish)
else:
    print("No menu items found.")



"""Testing Get Order Time"""
order_id = 11
print("Test: Retrieving Order Time for a Valid Order ID")
order_time = db.get_order_time(order_id)
if order_time:
    print(f"Order time for order_id {order_id}: {order_time}")
else:
    print(f"No order found for order_id {order_id}")


"""Testing Get Delivery Person Status"""
delivery_person_status = db.get_delivery_person_status()

if delivery_person_status:
    print("Deliverymen Status:")
    for delivery_person in delivery_person_status:
        print(f"ID: {delivery_person['id']}, Name: {delivery_person['name']}, Postcode: {delivery_person['postcode']}, Available Time: {delivery_person['time']}")
else:
    print("No delivery person found or error fetching data.")

"""===================== Testing Coupon Related Methods ====================="""

# --- Test 1: Checking if the customer has enough points for a coupon ---
print("Test 1: Check if customer has enough points for a coupon")

customer_id = 1

# Set up scenario: Assume the customer has 10 accumulated points
db.cursor.execute("UPDATE customer SET accumulation = 10 WHERE customer_id = %s", (customer_id,))
db.conn.commit()

# Check if the customer is eligible for a coupon
has_coupon = db.check_coupon(customer_id)
if has_coupon:
    print(f"Customer {customer_id} is eligible for a coupon.")
else:
    print(f"Customer {customer_id} is NOT eligible for a coupon.")

# Check if accumulation is reduced correctly
db.cursor.execute("SELECT accumulation FROM customer WHERE customer_id = %s", (customer_id,))
accumulation = db.cursor.fetchone()[0]
if accumulation == 0:
    print(f"Accumulation points successfully reduced to {accumulation}.")
else:
    print(f"Accumulation points were not updated correctly. Current accumulation: {accumulation}.")


# --- Test 2: Issuing a coupon ---
print("\nTest 2: Issuing a new coupon to the customer")

# Assume customer has accumulated enough points for a coupon
db.issue_coupon(customer_id)

# Verify that a coupon was added to the coupon table for this customer
db.cursor.execute("SELECT coupon_id FROM coupon WHERE customer_id = %s", (customer_id,))
issued_coupon = db.cursor.fetchone()
if issued_coupon:
    print(f"Coupon issued successfully with coupon_id: {issued_coupon[0]}")
else:
    print("Failed to issue a coupon.")


# --- Test 3: Checking if the customer has a valid coupon ---
print("\nTest 3: Checking if the customer has a valid coupon")

# Check if the customer has a valid coupon
coupon_info = db.has_valid_coupon(customer_id)
if coupon_info:
    print(f"Customer {customer_id} has a valid coupon with coupon_id: {coupon_info['coupon_id']}")
else:
    print(f"Customer {customer_id} does NOT have a valid coupon.")

# --- Test 4: Redeeming a coupon ---
print("\nTest 4: Redeeming a coupon")

# Assuming that the customer has a valid coupon
if coupon_info:
    print(coupon_info)
    coupon_id = coupon_info['coupon_id']
    print(coupon_id)
    redeemed = db.redeem_coupon(coupon_id)
    print(redeemed)
    if redeemed:
        print(f"Coupon {coupon_id} redeemed successfully.")

        # Verify that the coupon has been deleted after redemption
        db.cursor.execute("SELECT coupon_id FROM coupon WHERE coupon_id = %s", (coupon_id,))
        deleted_coupon = db.cursor.fetchone()
        if not deleted_coupon:
            print(f"Coupon {coupon_id} was successfully deleted after being redeemed.")
        else:
            print(f"Coupon {coupon_id} still exists in the database and was not deleted.")
    else:
        print(f"Failed to redeem coupon {coupon_id}.")
else:
    print(f"No valid coupon found for customer {customer_id}. Cannot proceed with redemption test.")


# Test for `get_order_status`
print("Test: Get Order Status for Existing Orders")
test_order_ids = [4, 7, 13]  # Replace these IDs with existing orders in your database
db.get_order_status(test_order_ids)

# Test for `assign_delivery_person`
print("\nTest: Assign Delivery Person to an Order")

# Assume we have a valid order ID and postal code
test_order_id = 11  # Replace with an actual order ID in your database

success = db.assign_delivery_person(test_order_id)
if success:
    print(f"Delivery person successfully assigned to order {test_order_id}")
else:
    print(f"Failed to assign delivery person to order {test_order_id}")

# Specify the postcode for which you just inserted the orders
test_postcode = '6214AA'  # Ensure this matches the customer's postcode

print("Test: Group Delivery Orders")
success = db.group_delivery_orders(test_postcode)

if success:
    print(f"Orders for postal code {test_postcode} have been successfully grouped and assigned to a delivery person.")
else:
    print(f"Failed to group orders for postal code {test_postcode}.")