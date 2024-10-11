from utils.db_connection import create_connection
import datetime


class PizzaDatabase:
    # def __init__(self):
    #     self.conn = create_connection()
    #     self.cursor = self.conn.cursor() if self.conn else None
    #
    # def __del__(self):
    #     if self.conn:
    #         self.conn.close()

    def __init__(self):
        # Ensure that self.conn is always defined, even if the connection fails
        self.conn = create_connection()  # Try to create a connection
        if self.conn:
            self.cursor = self.conn.cursor()
        else:
            self.cursor = None  # No connection means no cursor

    def __del__(self):
        # Check if self.conn is defined and connected before trying to close it
        if hasattr(self, 'conn') and self.conn and self.conn.is_connected():
            try:
                self.conn.close()
                print("Database connection closed.")
            except Exception as e:
                print(f"Error closing connection: {e}")

    def get_pizza(self, id):
        self.cursor.execute(
            f"SELECT pizza.name, ingredient.ingredient_id FROM ingredient JOIN pizza_to_ingredient ON ingredient.ingredient_id = pizza_to_ingredient.ingredient_id JOIN pizza ON pizza.pizza_id = pizza_to_ingredient.pizza_id WHERE pizza.pizza_id = '{id}';")
        info = self.cursor.fetchall()
        return {"name": info[0][0], "ingredients": [p[1] for p in info]}

    def get_ingredient(self, id):
        self.cursor.execute("SELECT name, category, price FROM ingredient WHERE ingredient_id = '" + str(id) + "';")
        ingredient = self.cursor.fetchone()
        return {"name": ingredient[0], "category": ingredient[1], "price": ingredient[2]}

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
        - customer_id: The ID of the customer placing the order.
        - pizzas: A list of pizza IDs being ordered.
        - sidedishes: A list of side dish IDs being ordered.
        """
        try:
            # Start a transaction to place the order
            self.cursor.execute("INSERT INTO order_info (customer_id, time) VALUES (%s, %s)",
                                (customer_id, datetime.datetime.now()))
            self.conn.commit()

            # Get the last inserted order_id
            self.cursor.execute("SELECT LAST_INSERT_ID()")
            order_id = self.cursor.fetchone()[0]

            # Insert pizzas into the order_to_pizza table
            for pizza_id in pizzas:
                self.cursor.execute("INSERT INTO order_to_pizza (order_id, pizza_id) VALUES (%s, %s)",
                                    (order_id, pizza_id))
                # Update the accumulation of the customer
                self.cursor.execute("UPDATE customer SET accumulation = accumulation + 1 WHERE customer_id = %s",
                                    (customer_id,))

            # Insert side dishes into the order_to_sidedish table
            for dish_id in sidedishes:
                self.cursor.execute("INSERT INTO order_to_sidedish (order_id, sidedish_id) VALUES (%s, %s)",
                                    (order_id, dish_id))

            # Commit all changes
            self.conn.commit()

            return order_id
        except Exception as e:
            self.conn.rollback()
            print(f"Error placing order: {e}")
            return None

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
                order_info = {
                    "order_id": result[0],
                    "customer_name": result[1],
                    "time": result[2],
                    "address": result[3]
                }
                return order_info
            else:
                return None
        except Exception as e:
            print(f"Error retrieving order information: {e}")
            return None

    def get_menu_items(self):
        """
        Get a list of all available pizzas and side dishes.
        """
        try:
            self.cursor.execute("SELECT pizza_id, name, price FROM pizza")
            pizzas = [{"id": row[0], "name": row[1], "price": row[2]} for row in self.cursor.fetchall()]

            self.cursor.execute("SELECT sidedish_id, name, price FROM sidedish")
            sidedishes = [{"id": row[0], "name": row[1], "price": row[2]} for row in self.cursor.fetchall()]

            return {
                "pizzas": pizzas,
                "sidedishes": sidedishes
            }
        except Exception as e:
            print(f"Error getting menu items: {e}")
            return None

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

    def check_coupon(self, customer_id):
        """
        Check if the customer has a valid coupon for a discount.
        """
        query = "SELECT accumulation FROM customer WHERE customer_id = %s"
        try:
            self.cursor.execute(query, (customer_id,))
            result = self.cursor.fetchone()
            if result and result[0] >= 10:
                # The customer has enough points for a coupon, update the accumulation
                update_query = "UPDATE customer SET accumulation = accumulation - 10 WHERE customer_id = %s"
                self.cursor.execute(update_query, (customer_id,))
                self.conn.commit()
                return True
            return False
        except Exception as e:
            self.conn.rollback()
            print(f"Error checking coupon: {e}")
            return False


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
        Get the current status of all delivery persons.
        """
        try:
            self.cursor.execute("SELECT delivery_person_id, name, postcode, time FROM delivery_person")
            delivery_person = self.cursor.fetchall()
            return [{"id": d[0], "name": d[1], "postcode": d[2], "time": d[3]} for d in delivery_person]
        except Exception as e:
            print(f"Error fetching deliverymen status: {e}")
            return []

    def get_order_status(self, order_ids):
        """
        Get the status of the specified orders.

        Args:
            order_ids (list): List of order IDs to check status for.
        """
        try:
            for order_id in order_ids:
                # Check if the order exists
                self.cursor.execute("SELECT time FROM order_info WHERE order_id = %s", (order_id,))
                result = self.cursor.fetchone()

                if not result:
                    print(f"Order {order_id} does not exist or has been cancelled.")
                    continue

                order_time = result[0]
                time_diff = (datetime.datetime.now() - order_time).total_seconds()

                # Determine the order status based on the elapsed time
                if time_diff < 600:  # less than 10 minutes
                    print(f"Your order {order_id} is being prepared.")
                    estimated_delivery = order_time + datetime.timedelta(minutes=10)
                    print(f"It will be delivered around {estimated_delivery.strftime('%Y-%m-%d %H:%M')}")
                elif time_diff < 1800:  # between 10 and 30 minutes
                    print(f"Your order {order_id} is out for delivery.")
                    estimated_arrival = order_time + datetime.timedelta(minutes=30)
                    print(f"It will arrive around {estimated_arrival.strftime('%Y-%m-%d %H:%M')}")
                else:
                    print(f"Your order {order_id} has been delivered.")

        except Exception as e:
            print(f"Error retrieving order status: {e}")

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
            # Create a new customer with default accumulation of 1
            self.cursor.execute(query, (name, gender, birthday, address, postcode, phone, 1))
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

