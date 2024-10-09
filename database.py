from utils.db_connection import create_connection
import datetime


class PizzaDatabase:
    def __init__(self):
        self.conn = create_connection()
        self.cursor = self.conn.cursor() if self.conn else None

    def __del__(self):
        if self.conn:
            self.conn.close()

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
                    "ingredients": ingredient_id_list,  # 使用配料 ID 列表
                    "ingredient_names": ingredients  # 配料名称字符串
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

