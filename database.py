from utils.db_connection import create_connection
import datetime


class PizzaDatabase:

    def __init__(self):
        self.conn = create_connection()
        self.cursor = self.conn.cursor()

    def __del__(self):
        if self.conn:
            try:
                if self.conn.is_connected():
                    self.cursor.close()
                    self.conn.close()
                    print("Connection closed.")
            except Exception as e:
                print(f"Error during connection cleanup: {e}")

    def get_pizza(self, pizza_id):
        self.cursor.execute("""
            SELECT pizza.name, ingredient.ingredient_id 
            FROM ingredient 
            JOIN pizza_to_ingredient ON ingredient.ingredient_id = pizza_to_ingredient.ingredient_id 
            JOIN pizza ON pizza.pizza_id = pizza_to_ingredient.pizza_id 
            WHERE pizza.pizza_id = %s;
        """, (pizza_id,))
        info = self.cursor.fetchall()
        return {
            "name": info[0][0],
            "ingredients": [int(p[1]) for p in info]
        }

    def get_ingredient(self, id):
        """
        Fetch the ingredient's details from the database, considering 'VEGETABLE' as vegan.
        """
        try:
            self.cursor.execute("SELECT name, category, price FROM ingredient WHERE ingredient_id = %s", (id,))
            ingredient = self.cursor.fetchone()
            if ingredient:
                is_vegan = ingredient[1].upper() == "VEGETABLE"  # Check if the category is VEGETABLE
                return {"name": ingredient[0], "category": ingredient[1], "price": ingredient[2], "vegan": is_vegan}
            else:
                print(f"Warning: Ingredient with ID {id} not found.")
                return {"name": "Unknown", "category": "Unknown", "price": 0, "vegan": False}  # Default values
        except Exception as e:
            print(f"Error fetching ingredient with ID {id}: {e}")
            return {"name": "Error", "category": "Error", "price": 0, "vegan": False}

    def get_side_dish(self, id):
        self.cursor.execute(f"SELECT name, price FROM sidedish WHERE sidedish_id= {id};")
        side_dish = self.cursor.fetchone()
        return {"name": side_dish[0], "price": side_dish[1]}

    def login(self, username, password):
        """
        Validate user login using username and password.
        """
        query = "SELECT customer_id FROM users WHERE username = %s AND password = %s"
        try:
            self.cursor.execute(query, (username, password))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error during login: {e}")
            return None

    def get_customer_info(self, customer_id):
        """
        Get customer information based on customer ID.
        """
        query = """
            SELECT name, gender, birthday, phone, address, postcode, accumulation
            FROM customer
            WHERE customer_id = %s
        """
        try:
            self.cursor.execute(query, (customer_id,))
            result = self.cursor.fetchone()
            if result:
                customer_info = {
                    "name": result[0],
                    "gender": result[1],
                    "birthday": result[2],
                    "phone": result[3],
                    "address": result[4],
                    "postcode": result[5],
                    "accumulation": result[6]
                }
                return customer_info
            else:
                return None
        except Exception as e:
            print(f"Error getting customer information: {e}")
            return None

    def place_order(self, customer_id, pizzas, sidedishes):
        """
        Place a new order for the customer.
        """
        try:
            # Start a transaction to place the order
            self.cursor.execute("INSERT INTO order_info (customer_id, time) VALUES (%s, %s)",
                                (customer_id, datetime.datetime.now()))
            self.conn.commit()

            # Get the last inserted order_id
            self.cursor.execute("SELECT LAST_INSERT_ID()")
            order_id = self.cursor.fetchone()[0]

            total_pizzas_ordered = 0  # Initialize total pizzas ordered

            # Insert pizzas into the order_to_pizza table with quantities
            for pizza_id, quantity in pizzas.items():
                self.cursor.execute(
                    "INSERT INTO order_to_pizza (order_id, pizza_id, quantity) VALUES (%s, %s, %s)",
                    (order_id, pizza_id, quantity))
                total_pizzas_ordered += quantity  # Accumulate the number of pizzas ordered

            # Insert side dishes into the order_to_sidedish table with quantities
            for dish_id, quantity in sidedishes.items():
                self.cursor.execute(
                    "INSERT INTO order_to_sidedish (order_id, sidedish_id, quantity) VALUES (%s, %s, %s)",
                    (order_id, dish_id, quantity))

            # Update the accumulation of the customer
            self.cursor.execute(
                "UPDATE customer SET accumulation = accumulation + %s WHERE customer_id = %s",
                (total_pizzas_ordered, customer_id))

            # Commit all changes
            self.conn.commit()

            return order_id
        except Exception as e:
            self.conn.rollback()
            print(f"Error placing order: {e}")
            return None

    def get_customer_accumulation(self, customer_id):
        """
        Get the customer's current accumulation.
        """
        query = "SELECT accumulation FROM customer WHERE customer_id = %s"
        try:
            self.cursor.execute(query, (customer_id,))
            result = self.cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error getting customer accumulation: {e}")
            return 0

    def reset_customer_accumulation(self, customer_id, new_accumulation):
        """
        Reset the customer's accumulation to a new value.
        """
        query = "UPDATE customer SET accumulation = %s WHERE customer_id = %s"
        try:
            self.cursor.execute(query, (new_accumulation, customer_id))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Error resetting customer accumulation: {e}")

    def get_order_info(self, order_id):
        """
        Get details of a specific order.
        """
        query = """
            SELECT o.order_id, c.name, o.time, c.address
            FROM order_info o
            JOIN customer c ON o.customer_id = c.customer_id
            WHERE o.order_id = %s
        """
        try:
            self.cursor.execute(query, (order_id,))
            result = self.cursor.fetchone()
            if result:
                return {
                    "order_id": result[0],
                    "customer_name": result[1],
                    "time": result[2],
                    "address": result[3]
                }
            return None
        except Exception as e:
            print(f"Error retrieving order information: {e}")
            return None

    def get_menu_items(self):
        """
        Get a list of all available pizzas and side dishes.
        Pizzas are priced based on their ingredients and include a list of ingredients.
        """
        try:
            # Dictionary to hold the pizzas
            pizzas = []

            # Fetch pizzas and their ingredients with prices and IDs
            self.cursor.execute("""
                SELECT p.pizza_id, p.name, SUM(i.price) AS total_price, GROUP_CONCAT(i.ingredient_id SEPARATOR ',') AS ingredient_ids, GROUP_CONCAT(i.name SEPARATOR ', ') AS ingredients
            FROM pizza p
            JOIN pizza_to_ingredient pi ON p.pizza_id = pi.pizza_id
            JOIN ingredient i ON pi.ingredient_id = i.ingredient_id
            GROUP BY p.pizza_id, p.name
            """)

            # Collect the pizza details including the name, price, and ingredients
            for row in self.cursor.fetchall():
                pizza_id, pizza_name, total_ingredient_price, ingredient_ids, ingredients = row
                # Add a 40% profit margin and 9% VAT to the total ingredient cost
                price_with_profit = total_ingredient_price * 1.40
                price_with_vat = price_with_profit * 1.09
                # Convert ingredient_ids string to list of integers
                ingredient_id_list = [int(x) for x in ingredient_ids.split(',')]
                pizzas.append({
                    "id": pizza_id,
                    "name": pizza_name,
                    "price": price_with_vat,
                    "ingredients": ingredient_id_list,
                    "ingredient_names": ingredients
                })

            # Fetch side dishes from the database
            self.cursor.execute("SELECT sidedish_id, name, price FROM sidedish")
            sidedishes = [{"id": row[0], "name": row[1], "price": row[2]} for row in self.cursor.fetchall()]

            # Return pizzas and side dishes as a dictionary
            return {
                "pizzas": pizzas,
                "sidedishes": sidedishes
            }
        except Exception as e:
            # Handle error by printing the exception and returning empty lists
            print(f"Error getting menu items: {e}")
            return {"pizzas": [], "sidedishes": []}

    def get_order_time(self, order_id):
        """
        Get the time when the order was placed.
        """
        try:
            self.cursor.execute("SELECT time FROM order_info WHERE order_id = %s", (order_id,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            print(f"Error retrieving order time: {e}")
            return None

    def get_customer_orders(self, customer_id):
        """
        Get all orders for a specific customer.
        """
        try:
            self.cursor.execute("""
                SELECT order_id, time 
                FROM order_info
                WHERE customer_id = %s
            """, (customer_id,))
            orders = self.cursor.fetchall()

            # Format orders into a list of dictionaries
            return [{"order_id": order[0], "time": order[1]} for order in orders]
        except Exception as e:
            print(f"Error retrieving customer orders: {e}")
            return []

    def get_customer_id_from_order(self, order_id):
        """
        Get the customer ID associated with an order.
        """
        try:
            self.cursor.execute("SELECT customer_id FROM order_info WHERE order_id = %s", (order_id,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            print(f"Error retrieving customer ID: {e}")
            return None

    def id_exists(self, table, id):
        """
        Check if a given ID exists in the specified table.
        """
        try:
            query = f"SELECT 1 FROM {table} WHERE order_id = %s LIMIT 1"
            self.cursor.execute(query, (id,))
            return self.cursor.fetchone() is not None
        except Exception as e:
            print(f"Error checking ID existence: {e}")
            return False

    def cancel_order(self, order_id):
        """
        Cancel an existing order.
        """
        try:
            # Check if the order exists
            if not self.id_exists("order_info", order_id):
                print(f"Order {order_id} doesn't exist. Please try again.")
                return

            # Check if it's within 5 minutes of placing the order
            order_time = self.get_order_time(order_id)
            if order_time:
                current_time = datetime.datetime.now()
                if current_time > order_time + datetime.timedelta(minutes=5):
                    print(f"Cannot cancel order {order_id} because more than 5 minutes have passed.")
                    return

            # Get the customer ID associated with the order
            customer_id = self.get_customer_id_from_order(order_id)
            if not customer_id:
                print(f"Unable to retrieve customer ID for order {order_id}.")
                return

            # Proceed to cancel the order
            # First, delete linked pizzas and side dishes
            self.cursor.execute("DELETE FROM order_to_pizza WHERE order_id = %s", (order_id,))
            self.cursor.execute("DELETE FROM order_to_sidedish WHERE order_id = %s", (order_id,))

            # Then delete the order itself
            self.cursor.execute("DELETE FROM order_info WHERE order_id = %s", (order_id,))

            # Update the customer's accumulation by subtracting 1
            self.cursor.execute("UPDATE customer SET accumulation = accumulation - 1 WHERE customer_id = %s", (customer_id,))

            # Commit the changes to the database
            self.conn.commit()
            print(f"Order {order_id} has been cancelled and accumulation has been adjusted.")

        except Exception as e:
            # Roll back if an error occurs
            self.conn.rollback()
            print(f"Error cancelling order: {e}")

    def check_coupon(db, customer_id):
        """
        Automatically apply a 10% discount if the customer has accumulated 10 or more pizzas.
        """
        # Get the customer's current accumulation
        accumulation = db.get_customer_accumulation(customer_id)
        if accumulation >= 10:
            print("- Congratulations! You've ordered 10 or more pizzas and earned a 10% discount on this order.")
            # Reset accumulation by subtracting 10
            new_accumulation = accumulation - 10
            db.reset_customer_accumulation(customer_id, new_accumulation)
            return 0.9  # Apply 10% discount
        else:
            pizzas_needed = 10 - accumulation
            print(f"- You need {pizzas_needed} more pizza(s) to earn a 10% discount on your next order.")
        return 1.0  # No discount

    def issue_coupon(self, customer_id):
        """
        Issue a new coupon to the customer if eligible.
        """
        query = """
            INSERT INTO coupon (customer_id, discount_percentage)
            VALUES (%s, %s)
        """
        try:
            self.cursor.execute(query, (customer_id, 0.1))  # 10% discount
            self.conn.commit()
            print("Coupon issued successfully.")
        except Exception as e:
            self.conn.rollback()
            print(f"Error issuing coupon: {e}")

    def has_valid_coupon(self, customer_id):
        """
        Check if a customer has a valid coupon.
        """
        query = """
            SELECT coupon_id, discount_percentage
            FROM coupon
            WHERE customer_id = %s
        """
        try:
            self.cursor.execute(query, (customer_id,))
            result = self.cursor.fetchone()
            if result:
                return {"coupon_id": result[0], "discount_percentage": result[1]}
            return None
        except Exception as e:
            print(f"Error checking coupon: {e}")
            return None

    def redeem_coupon(self, coupon_id):
        """
        Redeem a coupon for the current order.
        """
        try:
            # Check if the coupon exists in the database
            self.cursor.execute("SELECT coupon_id FROM coupon WHERE coupon_id = %s", (coupon_id,))
            coupon = self.cursor.fetchone()
            if not coupon:
                print("Invalid coupon.")
                return False

            # Delete the coupon after it's redeemed
            self.cursor.execute("DELETE FROM coupon WHERE coupon_id = %s", (coupon_id,))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error redeeming coupon: {e}")
            return False

    def get_delivery_person_status(self):
        """
        Get the current status of all delivery persons, resetting their time if it's in the past.
        """
        try:
            # Fetch all delivery persons
            self.cursor.execute("SELECT delivery_person_id, name, postcode, time FROM delivery_person")
            delivery_persons = self.cursor.fetchall()
            updated_delivery_persons = []

            for dp in delivery_persons:
                dp_id, dp_name, dp_postcode, dp_time = dp
                if dp_time and dp_time <= datetime.datetime.now():
                    # Reset time to NULL in the database
                    self.cursor.execute("""
                        UPDATE delivery_person
                        SET time = NULL
                        WHERE delivery_person_id = %s
                    """, (dp_id,))
                    self.conn.commit()
                    dp_time = None  # Update the local variable to reflect the change
                updated_delivery_persons.append({
                    "id": dp_id,
                    "name": dp_name,
                    "postcode": dp_postcode,
                    "time": dp_time
                })
            return updated_delivery_persons
        except Exception as e:
            print(f"Error fetching delivery person status: {e}")
            return []

    def get_order_status(self, order_ids):
        """
        Get the status of the specified orders.
        """
        try:
            for order_id in order_ids:
                self.cursor.execute("SELECT time FROM order_info WHERE order_id = %s", (order_id,))
                result = self.cursor.fetchone()

                if not result:
                    return f"Order {order_id} does not exist or has been cancelled."

                order_time = result[0]
                time_diff = (datetime.datetime.now() - order_time).total_seconds()

                if time_diff < 600:  # less than 10 minutes
                    return f"Order {order_id} is being prepared."
                elif time_diff < 1800:  # between 10 and 30 minutes
                    return f"Order {order_id} is out for delivery."
                else:
                    return f"Order {order_id} has been delivered."
        except Exception as e:
            print(f"Error retrieving order status: {e}")
            return "Error retrieving order status."

    def assign_delivery_person(self, order_id):
        """
        Assign a delivery person to an order based on the customer's postal code.
        """
        try:
            # Step 1: Retrieve the customer_id from the order_info table for the given order_id
            self.cursor.execute("SELECT customer_id FROM order_info WHERE order_id = %s", (order_id,))
            order_info = self.cursor.fetchone()

            if not order_info:
                print(f"No order found with ID {order_id}.")
                return False

            customer_id = order_info[0]

            # Step 2: Retrieve the customer's postal code from the customer table
            self.cursor.execute("SELECT postcode FROM customer WHERE customer_id = %s", (customer_id,))
            customer_info = self.cursor.fetchone()

            if not customer_info:
                print(f"No customer found with ID {customer_id}.")
                return False

            postcode = customer_info[0]

            # Step 3: Find available delivery personnel for the given postal code
            self.cursor.execute("""
                SELECT delivery_person_id, time FROM delivery_person 
                WHERE postcode = %s AND (time IS NULL OR time <= %s)
                ORDER BY time ASC LIMIT 1
            """, (postcode, datetime.datetime.now()))
            delivery_person = self.cursor.fetchone()

            if not delivery_person:
                print(f"No delivery person available for postal code {postcode}.")
                return False

            delivery_person_id, current_time = delivery_person
            estimated_delivery_time = datetime.datetime.now() + datetime.timedelta(minutes=30)

            # Step 4: Update delivery person time to make them unavailable for the next 30 minutes
            self.cursor.execute("""
                UPDATE delivery_person 
                SET time = %s 
                WHERE delivery_person_id = %s
            """, (estimated_delivery_time, delivery_person_id))
            self.conn.commit()

            # Step 5: Assign the delivery person to the order
            self.cursor.execute("""
                UPDATE order_info 
                SET delivery_person_id = %s 
                WHERE order_id = %s
            """, (delivery_person_id, order_id))
            self.conn.commit()

            print(f"Order {order_id} assigned to delivery person {delivery_person_id}.")
            return True

        except Exception as e:
            self.conn.rollback()
            print(f"Error assigning delivery person: {e}")
            return False

    def group_delivery_orders(self, postcode):
        """
        Group orders for the same postal code into a single delivery if they occur within a 3-minute window.
        Maximum of 3 pizzas per delivery.
        """
        try:
            # Find all orders within a 3-minute window and the same postal code
            self.cursor.execute("""
                SELECT order_info.order_id, order_info.customer_id, order_info.time 
                FROM order_info 
                JOIN customer ON order_info.customer_id = customer.customer_id
                WHERE customer.postcode = %s 
                AND (order_info.time >= %s AND order_info.time <= %s)
                AND order_info.delivery_person_id IS NULL
                LIMIT 3
            """, (postcode, datetime.datetime.now() - datetime.timedelta(minutes=3), datetime.datetime.now()))

            orders = self.cursor.fetchall()
            print(orders)

            if len(orders) == 0:
                print(f"No orders found within a 3-minute window for postal code {postcode}.")
                return False

            # Find an available delivery person for the given postal code
            self.cursor.execute("""
                            SELECT delivery_person_id, time FROM delivery_person 
                            WHERE postcode = %s AND (time IS NULL OR time <= %s)
                            ORDER BY time ASC LIMIT 1
                        """, (postcode, datetime.datetime.now()))
            delivery_person = self.cursor.fetchone()

            if not delivery_person:
                print(f"No delivery person available for postal code {postcode}.")
                return False



            delivery_person_id, current_time = delivery_person
            estimated_delivery_time = datetime.datetime.now() + datetime.timedelta(minutes=30)

            # Update delivery person time to make them unavailable for the next 30 minutes
            self.cursor.execute("""
                UPDATE delivery_person 
                SET time = %s 
                WHERE delivery_person_id = %s
            """, (estimated_delivery_time, delivery_person_id))
            self.conn.commit()

            # Assign the delivery person to the group of orders
            for order in orders:
                order_id = order[0]
                self.cursor.execute("""
                    UPDATE order_info 
                    SET delivery_person_id = %s 
                    WHERE order_id = %s
                """, (delivery_person_id, order_id))
                self.conn.commit()

            print(
                f"Orders {', '.join([str(order[0]) for order in orders])} have been grouped and assigned to delivery person {delivery_person_id}.")
            return True

        except Exception as e:
            self.conn.rollback()
            print(f"Error grouping delivery orders: {e}")
            return False

    def reset_orders(self):
        """
        Reset the order-related tables: order_info, order_to_pizza, order_to_sidedish.
        Also reset the accumulation in the customer table.
        """
        try:
            # Start a transaction
            self.conn.start_transaction()
            # Delete all records from order-related tables
            self.cursor.execute("DELETE FROM order_to_pizza")
            self.cursor.execute("DELETE FROM order_to_sidedish")
            self.cursor.execute("DELETE FROM order_info")
            # Reset AUTO_INCREMENT value for order_info table
            self.cursor.execute("ALTER TABLE order_info AUTO_INCREMENT = 1")
            # Reset accumulation in customer table
            self.cursor.execute("UPDATE customer SET accumulation = 0")
            # Commit the transaction
            self.conn.commit()
            print("All orders have been reset. Next order ID will start from 1.")
        except Exception as e:
            self.conn.rollback()
            print(f"Error resetting orders: {e}")
    def exists(self, table, column, value):
        """
        Check if a value exists in a specific table column.

        Args:
            table (str): Table name to query.
            column (str): Column name to check.
            value (str): The value to check for.

        Returns:
            bool: True if the value exists, False otherwise.
        """
        query = f"SELECT 1 FROM {table} WHERE {column} = %s LIMIT 1"
        try:
            self.cursor.execute(query, (value,))
            result = self.cursor.fetchone()  # Store the result
            return result is not None  # Check if any result is fetched
        except Exception as e:
            print(f"Error checking existence in table '{table}' for column '{column}': {e}")
            return False

    def create_customer(self, name, gender, birthday, address, postcode, phone):
        """
        Create a new customer in the database with an initial accumulation of 0.

        Args:
            name (str): Customer's name.
            gender (str): Customer's gender.
            birthday (str): Customer's birthday in 'YYYY-MM-DD' format.
            address (str): Customer's address.
            postcode (str): Customer's postcode.
            phone (str): Customer's phone number.

        Returns:
            int: The newly created customer_id.
        """
        query = """
            INSERT INTO customer (name, gender, birthday, address, postcode, phone, accumulation)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        try:
            # Create a new customer with default accumulation of 0
            self.cursor.execute(query, (name, gender, birthday, address, postcode, phone, 0))
            self.conn.commit()

            # Fetch the newly created customer_id
            self.cursor.execute("SELECT LAST_INSERT_ID()")
            customer_id = self.cursor.fetchone()[0]
            return customer_id
        except Exception as e:
            self.conn.rollback()
            print(f"Error creating customer: {e}")
            return None

    def get_pizza_status(self, pizza_id):
        """
        Check if the pizza is vegetarian or vegan based on its ingredients.

        Args:
            pizza_id (int): ID of the pizza.

        Returns:
            dict: A dictionary indicating if the pizza is vegetarian or vegan.
        """
        try:
            # Fetch the ingredients for the pizza
            self.cursor.execute("""
                SELECT ingredient.category 
                FROM ingredient
                JOIN pizza_to_ingredient ON ingredient.ingredient_id = pizza_to_ingredient.ingredient_id
                WHERE pizza_to_ingredient.pizza_id = %s
            """, (pizza_id,))
            ingredients = self.cursor.fetchall()

            # Check if the pizza contains any MEAT ingredients
            contains_meat = any(ingredient[0] == 'MEAT' for ingredient in ingredients)
            contains_dairy = any(ingredient[0] == 'DAIRY' for ingredient in ingredients)

            # If the pizza contains meat, it is neither vegetarian nor vegan
            if contains_meat:
                return {"vegetarian": False, "vegan": False}

            # If the pizza contains dairy, it is vegetarian but not vegan
            if contains_dairy:
                return {"vegetarian": True, "vegan": False}

            # If it contains only vegetables, it is vegan
            return {"vegetarian": True, "vegan": True}

        except Exception as e:
            print(f"Error checking pizza status: {e}")
            return {"vegetarian": False, "vegan": False}

    def get_customer_pizza_orders(self, customer_id):
        """
        Get all pizzas the customer has ordered, along with quantities.
        """
        try:
            # First, get all orders for the customer
            self.cursor.execute("""
                SELECT order_id
                FROM order_info
                WHERE customer_id = %s
            """, (customer_id,))
            orders = self.cursor.fetchall()
            if not orders:
                return []

            order_ids = [order[0] for order in orders]

            # Now, get pizzas and quantities for these orders
            # Use IN clause to get data for multiple order_ids
            format_strings = ','.join(['%s'] * len(order_ids))
            query = f"""
                SELECT otp.pizza_id, p.name, SUM(otp.quantity) as total_quantity
                FROM order_to_pizza otp
                JOIN pizza p ON otp.pizza_id = p.pizza_id
                WHERE otp.order_id IN ({format_strings})
                GROUP BY otp.pizza_id, p.name
            """
            self.cursor.execute(query, tuple(order_ids))
            pizzas = self.cursor.fetchall()
            # pizzas is a list of tuples (pizza_id, pizza_name, total_quantity)
            return pizzas
        except Exception as e:
            print(f"Error retrieving customer pizza orders: {e}")
            return []

    def get_pizzas_still_in_oven(self):
        """
        Retrieve pizzas that have been ordered but not yet dispatched for delivery.
        """
        try:
            # Fetch orders that have not been assigned to a delivery person yet
            self.cursor.execute("""
                SELECT oi.order_id, otp.pizza_id, p.name AS pizza_name, otp.quantity, oi.time AS order_time
                FROM order_info oi
                JOIN order_to_pizza otp ON oi.order_id = otp.order_id
                JOIN pizza p ON otp.pizza_id = p.pizza_id
                WHERE oi.delivery_person_id IS NULL
                ORDER BY oi.time ASC
            """)
            result = self.cursor.fetchall()
            pizzas_in_oven = []
            for row in result:
                pizzas_in_oven.append({
                    'order_id': row[0],
                    'pizza_id': row[1],
                    'pizza_name': row[2],
                    'quantity': row[3],
                    'order_time': row[4]
                })
            return pizzas_in_oven
        except Exception as e:
            print(f"Error retrieving pizzas still in oven: {e}")
            return []

    def assign_delivery_person2(self):
        """
        for handle group order, may not be the most efficient and elegant one, but it works
        """
        try:
            cutoff_time = datetime.datetime.now() - datetime.timedelta(minutes=3)

            # Find all unassigned orders older than 3 minutes
            self.cursor.execute("""
                SELECT oi.order_id, c.postcode, oi.time
                FROM order_info oi
                JOIN customer c ON oi.customer_id = c.customer_id
                WHERE oi.delivery_person_id IS NULL
                AND oi.time <= %s
                ORDER BY c.postcode, oi.time
            """, (cutoff_time,))

            pending_orders = self.cursor.fetchall()

            # Group orders by postal code
            orders_by_postcode = {}
            for order_id, postcode, order_time in pending_orders:
                if postcode not in orders_by_postcode:
                    orders_by_postcode[postcode] = []
                orders_by_postcode[postcode].append((order_id, order_time))

            # Assign delivery persons to grouped orders
            for postcode, orders in orders_by_postcode.items():
                self.group_and_assign_orders(orders, postcode)

            print("Delivery persons have been assigned to pending orders.")
            return True

        except Exception as e:
            self.conn.rollback()
            print(f"Error assigning delivery persons: {e}")
            return False

    def group_and_assign_orders(self, orders, postcode):
        """
        Group orders within a 3-minute window and assign a delivery person.
        """
        grouped_orders = []
        group_start_time = None
        total_pizzas = 0

        for order_id, order_time in orders:
            if group_start_time is None:
                group_start_time = order_time
                grouped_orders.append(order_id)
                total_pizzas += self.get_total_pizzas_in_order(order_id)
            else:
                time_diff = (order_time - group_start_time).total_seconds()
                if time_diff <= 180 and total_pizzas < 3:
                    # Within 3-minute window and pizza limit not exceeded
                    grouped_orders.append(order_id)
                    total_pizzas += self.get_total_pizzas_in_order(order_id)
                else:
                    # Assign the current group
                    self.assign_grouped_orders(grouped_orders, postcode)
                    # Reset grouping variables
                    group_start_time = order_time
                    grouped_orders = [order_id]
                    total_pizzas = self.get_total_pizzas_in_order(order_id)

        # Assign any remaining grouped orders
        if grouped_orders:
            self.assign_grouped_orders(grouped_orders, postcode)

    def get_total_pizzas_in_order(self, order_id):
        """
        Get the total number of pizzas in a specific order.
        """
        self.cursor.execute("""
            SELECT SUM(quantity)
            FROM order_to_pizza
            WHERE order_id = %s
        """, (order_id,))
        result = self.cursor.fetchone()
        return result[0] if result[0] else 0

    def assign_grouped_orders(self, order_ids, postcode):
        """
        Assign a delivery person to a group of orders.
        """
        # Find an available delivery person for the postcode
        self.cursor.execute("""
            SELECT delivery_person_id
            FROM delivery_person
            WHERE postcode = %s
            AND (time IS NULL OR time <= %s)
            ORDER BY time ASC
            LIMIT 1
        """, (postcode, datetime.datetime.now()))
        delivery_person = self.cursor.fetchone()

        if not delivery_person:
            print(f"No delivery person available for postal code {postcode}.")
            return False

        delivery_person_id = delivery_person[0]
        estimated_delivery_time = datetime.datetime.now() + datetime.timedelta(minutes=30)

        # Update delivery person time to make them unavailable for the next 30 minutes
        self.cursor.execute("""
            UPDATE delivery_person
            SET time = %s
            WHERE delivery_person_id = %s
        """, (estimated_delivery_time, delivery_person_id))
        self.conn.commit()

        # Assign the delivery person to the grouped orders
        for oid in order_ids:
            self.cursor.execute("""
                UPDATE order_info
                SET delivery_person_id = %s
                WHERE order_id = %s
            """, (delivery_person_id, oid))
        self.conn.commit()

        print(f"Orders {', '.join(map(str, order_ids))} have been assigned to delivery person {delivery_person_id}.")
        return True


    def generate_monthly_earnings_report(self, filters):
        """
        Generate a monthly earnings report with optional filters.
        Args:
            filters (dict): Filtering options for postcode, gender, and age range.
        Returns:
            dict: Report data including total earnings, order count, pizza count, and sidedish count.
        """
        try:
            # Get the first and last day of the current month
            today = datetime.date.today()
            first_day = today.replace(day=1)
            last_day = (first_day + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)

            # Pizza earnings query
            query = """
                SELECT
                    SUM(pizza_price * otp.quantity) AS total_price,
                    SUM(otp.quantity) AS total_quantity
                FROM order_info oi
                JOIN customer c ON oi.customer_id = c.customer_id
                JOIN order_to_pizza otp ON oi.order_id = otp.order_id
                -- Subquery to calculate the total price of each pizza based on its ingredients
                JOIN (
                    SELECT
                        pi.pizza_id,
                        SUM(i.price * 1.40 * 1.09) AS pizza_price
                    FROM pizza_to_ingredient pi
                    JOIN ingredient i ON pi.ingredient_id = i.ingredient_id
                    GROUP BY pi.pizza_id
                ) AS pizza_prices ON otp.pizza_id = pizza_prices.pizza_id
                WHERE oi.time BETWEEN %s AND %s
            """

            params = [first_day, last_day]

            # Apply filters
            if 'postcode' in filters:
                query += " AND c.postcode = %s"
                params.append(filters['postcode'])

            if 'gender' in filters:
                query += " AND c.gender = %s"
                params.append(filters['gender'])

            if 'age_min' in filters and 'age_max' in filters:
                today = datetime.date.today()
                birthdate_min = today.replace(year=today.year - filters['age_max'])
                birthdate_max = today.replace(year=today.year - filters['age_min'])
                query += " AND c.birthday BETWEEN %s AND %s"
                params.extend([birthdate_min, birthdate_max])

            # Group by aggregated values
            query += " GROUP BY oi.order_id"

            # Execute the query
            self.cursor.execute(query, tuple(params))
            pizza_orders = self.cursor.fetchall()

            # Now, get side dishes
            query_sidedish = """
                SELECT
                    SUM(sd.price * otd.quantity) AS sidedish_total_price,
                    SUM(otd.quantity) AS sidedish_quantity
                FROM order_info oi
                JOIN customer c ON oi.customer_id = c.customer_id
                JOIN order_to_sidedish otd ON oi.order_id = otd.order_id
                JOIN sidedish sd ON otd.sidedish_id = sd.sidedish_id
                WHERE oi.time BETWEEN %s AND %s
            """

            params_sidedish = [first_day, last_day]

            # Apply same filters
            if 'postcode' in filters:
                query_sidedish += " AND c.postcode = %s"
                params_sidedish.append(filters['postcode'])

            if 'gender' in filters:
                query_sidedish += " AND c.gender = %s"
                params_sidedish.append(filters['gender'])

            if 'age_min' in filters and 'age_max' in filters:
                query_sidedish += " AND c.birthday BETWEEN %s AND %s"
                params_sidedish.extend([birthdate_min, birthdate_max])

            query_sidedish += " GROUP BY oi.order_id"

            # Execute the query
            self.cursor.execute(query_sidedish, tuple(params_sidedish))
            sidedish_orders = self.cursor.fetchall()

            # Calculate totals
            total_earnings = 0.0
            pizza_count = 0
            sidedish_count = 0
            orders = set()

            # Process pizza orders
            for order in pizza_orders:
                pizza_total_price = order[0] if order[0] is not None else 0.0
                pizza_quantity = order[1] if order[1] is not None else 0

                total_earnings += pizza_total_price
                pizza_count += pizza_quantity

            # Process sidedish orders
            for order in sidedish_orders:
                sidedish_total_price = order[0] if order[0] is not None else 0.0
                sidedish_quantity = order[1] if order[1] is not None else 0

                total_earnings += sidedish_total_price
                sidedish_count += sidedish_quantity

            report = {
                'total_earnings': total_earnings,
                'order_count': len(pizza_orders) + len(sidedish_orders),
                'pizza_count': pizza_count,
                'sidedish_count': sidedish_count
            }

            return report if report['order_count'] > 0 else None

        except Exception as e:
            print(f"Error generating earnings report: {e}")
            return None


