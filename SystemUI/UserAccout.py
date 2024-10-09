from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from utils.db_connection import create_connection

class UserAccount:
    def __init__(self, main_window, customer_id):
        self.main_window = main_window
        self.customer_id = customer_id

    def show_my_account(self):
        # Clear the current screen
        self.main_window.clear_screen()

        # Setup "Customer Information" layout
        self.customer_info_widget = QWidget()
        self.customer_info_layout = QVBoxLayout()

        # Establish a connection to the database to fetch customer info
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # Fetch the customer's details using customer_id
                query = """
                    SELECT name, gender, birthday, phone, address, postcode, accumulation
                    FROM customer
                    WHERE customer_id = %s
                """
                cursor.execute(query, (self.customer_id,))
                customer_info = cursor.fetchone()

                if customer_info:
                    # Display customer information on the screen
                    self.greeting_label = QLabel(f"Account Details for {customer_info[0]}:", self.main_window)
                    self.greeting_label.setAlignment(Qt.AlignLeft)
                    self.greeting_label.setStyleSheet(
                        "font-size: 24px; font-weight: bold; color: white; background-color: red; padding: 10px; border-radius: 10px;")
                    self.customer_info_layout.addWidget(self.greeting_label)

                    # Add widgets to display other customer information with background styling
                    self.add_customer_info_label("Gender", customer_info[1])
                    self.add_customer_info_label("Birthday", customer_info[2])
                    self.add_customer_info_label("Phone", customer_info[3])
                    self.add_customer_info_label("Address", customer_info[4])
                    self.add_customer_info_label("Postcode", customer_info[5])
                    self.add_customer_info_label("You ordered", f"{customer_info[6]} times in the past.")

            except Exception as e:
                # Handle errors during the database interaction
                error_msg = QMessageBox()
                error_msg.setIcon(QMessageBox.Critical)
                error_msg.setText(f"An error occurred: {e}")
                error_msg.setWindowTitle("Account Info Error")
                error_msg.exec_()

            finally:
                conn.close()

        # Add a "Back" button to return to the main menu
        self.back_button = QPushButton('Back', self.main_window)
        self.back_button.setStyleSheet("font-size: 20px; font-weight: bold; font-style: italic; "
                                       "background-color: red; color:white; padding: 10px; border-radius: 10px;")
        self.back_button.setFixedSize(200, 50)
        self.back_button.clicked.connect(self.main_window.init_my_account_screen)  # Connect back to main menu
        self.customer_info_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

        # Set layout for "Customer Information" screen
        self.customer_info_widget.setLayout(self.customer_info_layout)
        self.main_window.setCentralWidget(self.customer_info_widget)

    def add_customer_info_label(self, label, value):
        """Helper method to add customer information labels."""
        info_label = QLabel(f"{label}: {value}", self.main_window)
        info_label.setStyleSheet(
            "font-size: 18px; color: black; background-color: lightyellow; padding: 5px; border-radius: 5px;")
        self.customer_info_layout.addWidget(info_label)
