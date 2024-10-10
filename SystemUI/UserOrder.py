# File: UserOrder.py

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox, QPushButton


class UserOrder:
    def __init__(self, main_window, customer_id, database):
        """
        Initialize the UserOrder class.
        :param main_window: Reference to the main application window.
        :param customer_id: The ID of the currently logged-in customer.
        :param database: Reference to the PizzaDatabase class for interacting with the database.
        """
        self.main_window = main_window
        self.customer_id = customer_id
        self.database = database  # Use database instance to fetch orders

    def show_my_order(self):
        """
        Display the orders for the logged-in user.
        """
        self.main_window.clear_screen()  # Clear the existing screen

        # Create layout for the "My Order" screen
        self.my_order_widget = QWidget()
        self.my_order_layout = QVBoxLayout()

        # Fetch orders for the logged-in user
        if self.customer_id:
            self.my_order_layout.addWidget(QLabel("My Orders:"))

            # Get all orders for the user
            orders = self.database.get_customer_orders(self.customer_id)

            # Display each order
            if orders:
                for order in orders:
                    order_info = self.database.get_order_info(order['order_id'])
                    order_status = self.database.get_order_status([order['order_id']])

                    # Create a label for each order
                    order_label = QLabel(f"Order ID: {order['order_id']}, Time: {order_info['time']}, "
                                         f"Status: {order_status}")
                    order_label.setStyleSheet("font-size: 14px; font-weight: bold;")
                    self.my_order_layout.addWidget(order_label)
            else:
                self.my_order_layout.addWidget(QLabel("No orders found."))

        else:
            # If no customer is logged in, display an error message
            error_label = QLabel("Please log in to view your orders.")
            error_label.setStyleSheet("font-size: 20px; color: red;")
            self.my_order_layout.addWidget(error_label)

        # Set up the layout and add it to the central widget
        self.my_order_widget.setLayout(self.my_order_layout)
        self.main_window.setCentralWidget(self.my_order_widget)

        # Add a "Back" button to return to the main window
        self.back_button = QPushButton('Back', self.main_window)
        self.back_button.setStyleSheet("font-size: 20px; font-weight: bold; font-style: italic; "
                                       "background-color: red; color:white; padding: 10px; border-radius: 10px;")
        self.back_button.setFixedSize(200, 50)
        self.back_button.clicked.connect(self.main_window.init_my_account_screen)  # Connect back to main menu
        self.my_order_layout.addWidget(self.back_button, alignment=Qt.AlignRight)

        # Set layout for "Customer Information" screen
        self.my_order_widget.setLayout(self.my_order_layout)
        self.main_window.setCentralWidget(self.my_order_widget)
