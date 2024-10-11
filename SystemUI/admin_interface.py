
#         # # Earnings Report Section
#         # self.report_label = QLabel("Generate Earnings Report")
#         # self.admin_layout.addWidget(self.report_label)
#         #
#         # self.region_input = QLineEdit(self)
#         # self.admin_layout.addWidget(QLabel("Enter Region (Postal Code or City):"))
#         # self.admin_layout.addWidget(self.region_input)
#         #
#         # self.filter_button = QPushButton("Generate Report", self)
#         # self.filter_button.clicked.connect(self.generate_report)
#         # self.admin_layout.addWidget(self.filter_button)
#         #
#         # # Delivery Personnel Management Section
#         # self.personnel_label = QLabel("Delivery Personnel Management")
#         # self.admin_layout.addWidget(self.personnel_label)
#         #
#         # self.assign_personnel_button = QPushButton("Assign Delivery Personnel", self)
#         # self.assign_personnel_button.clicked.connect(self.assign_personnel)
#         # self.admin_layout.addWidget(self.assign_personnel_button)
#
#         # Set the layout for the AdminPage widget
#         self.setLayout(self.admin_layout)
#

#
#     # def generate_report(self):
#     #     region = self.region_input.text()
#     #     # Query to generate earnings report based on the region
#     #     conn = create_connection()
#     #     cursor = conn.cursor()
#     #     query = "SELECT SUM(price) FROM orders WHERE region = %s"
#     #     cursor.execute(query, (region,))
#     #     total_earnings = cursor.fetchone()[0]
#     #     QMessageBox.information(self, "Earnings Report", f"Total Earnings for {region}: {total_earnings}")
#     #     conn.close()
#     #
#     # def assign_personnel(self):
#     #     # Logic to assign delivery personnel based on the area
#     #     conn = create_connection()
#     #     cursor = conn.cursor()
#     #     # Example query to find and assign delivery personnel
#     #     query = """
#     #     UPDATE delivery_person SET available = 'NO' WHERE delivery_person_id = (
#     #         SELECT delivery_person_id FROM delivery_person WHERE available = 'YES' LIMIT 1
#     #     )
#     #     """
#     #     cursor.execute(query)
#     #     conn.commit()
#     #     conn.close()
#     #     QMessageBox.information(self, "Success", "Delivery personnel assigned.")


from datetime import datetime
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QLineEdit, QPushButton, QTableWidgetItem, \
    QMessageBox
from utils.db_connection import create_connection
from database import PizzaDatabase

class AdminPage(QWidget):
    def __init__(self, parent=None):
        super(AdminPage, self).__init__(parent)
        self.admin_layout = QVBoxLayout(self)  # Initialize layout in the constructor
        self.db = PizzaDatabase()  # Create an instance of PizzaDatabase
        self.init_admin_interface()

    def init_admin_interface(self):
        # Clear the current screen (safely remove previous widgets)
        self.clear_screen()

        # Restaurant Monitoring Section
        self.monitoring_label = QLabel("Restaurant Monitoring - Undelivered Orders")
        self.admin_layout.addWidget(self.monitoring_label)

        self.monitor_orders_table = QTableWidget()
        self.monitor_orders_table.setColumnCount(3)
        self.monitor_orders_table.setHorizontalHeaderLabels(["Order ID", "Pizza", "Sidedish"])
        self.admin_layout.addWidget(self.monitor_orders_table)

        # Fetch and update the monitoring data
        self.update_monitoring()

        # Add Earnings Report Section
        self.add_earnings_report_section()

    def clear_screen(self):
        # Remove all widgets safely from the layout
        while self.admin_layout.count() > 0:
            child = self.admin_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()



    def update_monitoring(self):
        """
        Updates the restaurant monitoring table with undelivered orders
        and their statuses using the get_order_status method.
        """
        conn = create_connection()
        cursor = conn.cursor()

        try:
            # Step 1: Fetch all orders from the database, regardless of delivery status
            query = """
                SELECT oi.order_id, oi.customer_id, oi.time, 
                       GROUP_CONCAT(DISTINCT p.name SEPARATOR ', ') AS pizza_names,
                       GROUP_CONCAT(DISTINCT sd.name SEPARATOR ', ') AS sidedish_names
                FROM order_info oi
                LEFT JOIN order_to_pizza otp ON oi.order_id = otp.order_id
                LEFT JOIN pizza p ON otp.pizza_id = p.pizza_id
                LEFT JOIN order_to_sidedish otsd ON oi.order_id = otsd.order_id
                LEFT JOIN sidedish sd ON otsd.sidedish_id = sd.sidedish_id
                GROUP BY oi.order_id
            """
            cursor.execute(query)
            all_orders = cursor.fetchall()
            print(all_orders)

            # Set the table row count based on the number of orders
            self.monitor_orders_table.setRowCount(0)  # Clear the table

            # Step 2: Get the status for each order using get_order_status
            row_position = 0
            for order in all_orders:
                order_id, customer_id, order_time, pizza_names, sidedish_names = order

                # Use get_order_status to fetch the status and estimated delivery time
                order_status = self.db.get_order_status(order_id)

                # Only display orders that are not delivered yet
                if order_status["status"] in ["Being prepared"]:
                    # Add a new row in the table for each undelivered order
                    self.monitor_orders_table.insertRow(row_position)

                    # Populate the monitoring table with order details
                    self.monitor_orders_table.setItem(row_position, 0, QTableWidgetItem(str(order_id)))
                    self.monitor_orders_table.setItem(row_position, 1,
                                                      QTableWidgetItem(pizza_names or "No pizza ordered"))
                    self.monitor_orders_table.setItem(row_position, 2,
                                                      QTableWidgetItem(sidedish_names or "No side dishes"))

                    # Increment row_position after setting items for this row
                    row_position += 1
                    print(row_position)



        except Exception as e:
            print(f"Error updating monitoring: {e}")
        finally:
            conn.close()

    def add_earnings_report_section(self):
        """
        Adds the Earnings Report section with input fields for filtering by region, gender, and age.
        """
        # Earnings Report Section
        self.report_label = QLabel("Generate Monthly Earnings Report")
        self.admin_layout.addWidget(self.report_label)

        # Region input
        self.region_input = QLineEdit(self)
        self.region_input.setPlaceholderText("Enter Region (Postal Code or City)")
        self.admin_layout.addWidget(self.region_input)

        # Gender input
        self.gender_input = QLineEdit(self)
        self.gender_input.setPlaceholderText("Enter Gender (M/F)")
        self.admin_layout.addWidget(self.gender_input)

        # Age input
        self.age_input = QLineEdit(self)
        self.age_input.setPlaceholderText("Enter Age Range (e.g., 18-25)")
        self.admin_layout.addWidget(self.age_input)

        # Generate Report Button
        self.generate_report_button = QPushButton("Generate Report", self)
        self.generate_report_button.clicked.connect(self.generate_earnings_report)
        self.admin_layout.addWidget(self.generate_report_button)

    def generate_earnings_report(self):
        """
        Generates a monthly earnings report based on region, customer gender, and age range.
        """
        # Get the filter values from the input fields
        region = self.region_input.text()
        gender = self.gender_input.text()
        age_range = self.age_input.text()

        # Parse the age range
        try:
            age_min, age_max = map(int, age_range.split('-'))
        except ValueError:
            QMessageBox.critical(self, "Invalid Input", "Please enter a valid age range (e.g., 18-25).")
            return

        conn = create_connection()
        cursor = conn.cursor()

        try:
            # Query to calculate total earnings based on region, gender, and age range
            query = """
                   SELECT SUM(pd.final_price) AS total_earnings
                   FROM order_info oi
                   JOIN customer c ON oi.customer_id = c.customer_id
                   JOIN (
                       SELECT otp.order_id, SUM(p.price_with_profit + p.vat_amount) AS final_price
                       FROM order_to_pizza otp
                       JOIN pizza p ON otp.pizza_id = p.pizza_id
                       GROUP BY otp.order_id
                   ) pd ON oi.order_id = pd.order_id
                   WHERE c.region = %s AND c.gender = %s AND (YEAR(CURDATE()) - YEAR(c.birthday)) BETWEEN %s AND %s
                     AND MONTH(oi.time) = MONTH(CURDATE())  -- Filter for current month
               """
            cursor.execute(query, (region, gender, age_min, age_max))
            total_earnings = cursor.fetchone()[0]
            print(total_earnings)
            if total_earnings is not None:
                QMessageBox.information(self, "Earnings Report", f"Total Earnings: {total_earnings}")
            else:
                QMessageBox.information(self, "Earnings Report", "No earnings found for the given criteria.")

        except Exception as e:
            print(f"Error generating earnings report: {e}")
        finally:
            conn.close()

