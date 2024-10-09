import sys

from SystemUI.UserAccout import UserAccount
from SystemUI.checkout import Checkout
from SystemUI.menu import Menu
from utils.db_connection import create_connection
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, \
    QListWidget, QGraphicsLayout, QGridLayout, QTabWidget, QSpinBox, QTableWidget, QTableWidgetItem, QMessageBox


class PizzaOrderingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 600)
        self.setWindowTitle('Jay and Stella pizza order system')

        # Set background image using style sheet
        self.setStyleSheet("""
                    QMainWindow {
                        background-image: url('/Users/liaowenjie/PycharmProjects/DataBaseProject/pizza-7423546_1920.png');
                        background-repeat: no-repeat;
                        
                        background-position: center;
                    }
                """)
        # Initialize the login screen by default
        self.init_login_screen()

    def init_login_screen(self):
        # Create a login layout
        self.login_widget = QWidget()
        self.login_layout = QVBoxLayout()

        # Pizza image - Centered at the top
        self.pizza_image = QLabel(self)
        pixmap = QPixmap('/Iconarchive-Fat-Sugar-Food-Pizza.512.png')
        #adjust the size of the image
        pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio)
        self.pizza_image.setPixmap(pixmap)
        self.pizza_image.setAlignment(Qt.AlignCenter)  # Center the image
        self.login_layout.addWidget(self.pizza_image)

        # Welcome message - Centered below the image
        self.welcome_label = QLabel('Welcome to Jay and Stella\'s Pizza House!', self)
        self.welcome_label.setFixedWidth(600)

        self.login_layout.addWidget(self.welcome_label, alignment=Qt.AlignCenter)
        # Set larger, bold, and italic font
        self.welcome_label.setStyleSheet("" "font-size: 30px;"
                                         "font-weight: bold;"
                                         "color: white; font-style: italic; "
                                         "background-color: red;"
                                         "padding: 5px;"
                                         "width: auto;"
                                         "border-radius: 15px;")

        # Add the new label for login instructions
        self.login_instruction_label = QLabel('Please login with your account', self)
        self.login_instruction_label.setAlignment(Qt.AlignCenter)  # Center the text
        self.login_instruction_label.setStyleSheet(
            "font-size: 20px; font-style: chalkboard;")  # Set font size and style
        self.login_layout.addWidget(self.login_instruction_label)

        # Username input
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setFixedSize(250, 50)
        self.login_layout.addWidget(self.username_input, alignment=Qt.AlignCenter)  # Center in the layout

        # Password input
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedSize(250, 50)
        self.login_layout.addWidget(self.password_input, alignment=Qt.AlignCenter)  # Center in the layout

        # Login button
        self.login_button = QPushButton('Login', self)
        self.login_button.setFixedSize(150, 40)  # Adjust size
        self.login_button.clicked.connect(self.login)
        self.login_layout.addWidget(self.login_button, alignment=Qt.AlignCenter)  # Center in the layout

        # Set layout for the login screen
        self.login_widget.setLayout(self.login_layout)
        self.setCentralWidget(self.login_widget)

    # def login(self):
    #     # Handle user login logic (validate against your database for later)
    #     self.username = self.username_input.text()
    #     if self.username:
    #         # Proceed to pizza selection screen after login
    #         self.init_my_account_screen()

    def login(self):
        # Get the username and password from the input fields

        self.username = self.username_input.text()
        self.password = self.password_input.text()

        # Establish a connection to the MySQL database
        conn = create_connection()
        if conn:
            try:
                # Create a cursor to interact with the database
                cursor = conn.cursor()

                # Query to validate login credentials and get customer_id
                query = """
                    SELECT customer_id FROM users
                    WHERE username = %s AND password = %s
                """
                cursor.execute(query, (self.username, self.password))
                result = cursor.fetchone()

                # Check if login credentials are correct
                if result:
                    self.customer_id = result[0]  # Get the customer_id from the result
                    self.init_my_account_screen()  # Proceed to the account screen
                else:
                    # Display an error message if login fails
                    error_msg = QMessageBox()
                    error_msg.setIcon(QMessageBox.Critical)
                    error_msg.setText("Invalid username or password")
                    error_msg.setWindowTitle("Login Failed")
                    error_msg.exec_()

            except Exception as e:
                # Handle any errors that occur during the database interaction
                error_msg = QMessageBox()
                error_msg.setIcon(QMessageBox.Critical)
                error_msg.setText(f"An error occurred: {e}")
                error_msg.setWindowTitle("Login Error")
                error_msg.exec_()

            finally:
                # Close the database connection
                conn.close()
        else:
            # Display an error if the connection could not be established
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setText("Could not connect to the database. Please try again later.")
            error_msg.setWindowTitle("Connection Error")
            error_msg.exec_()

    def init_my_account_screen(self):
        # Clear the current screen
        self.clear_screen()

        # Setup "My Account" layout
        self.my_account_widget = QWidget()
        self.my_account_layout = QVBoxLayout()

        # Greeting text
        self.greeting_label = QLabel(f"Hi, {self.username}!", self)
        self.greeting_label.setAlignment(Qt.AlignLeft)
        self.greeting_label.setStyleSheet("font-size: 36px; font-weight: bold;")
        self.my_account_layout.addWidget(self.greeting_label)

        # Create buttons
        self.menu_button = QPushButton('Menu', self)
        self.menu_button.setStyleSheet("font-size: 20px; font-weight: bold; font-style: italic; "
                                       "background-color: red; color:white")
        self.menu_button.setFixedSize(200, 50)
        self.menu_button.clicked.connect(self.init_menu_screen)
        self.my_account_layout.addWidget(self.menu_button, alignment=Qt.AlignCenter)

        self.my_order_button = QPushButton('My Order', self)
        self.my_order_button.setStyleSheet("font-size: 20px; font-weight: bold; font-style: italic; "
                                           "background-color: red; color:white")
        self.my_order_button.setFixedSize(200, 50)
        #self.my_order_button.clicked.connect(self.show_my_order)

        self.my_account_layout.addWidget(self.my_order_button, alignment=Qt.AlignCenter)

        self.my_account_button = QPushButton('My Account', self)
        self.my_account_button.setStyleSheet("font-size: 20px; font-weight: bold; font-style: italic; "
                                             "background-color: red; color:white")
        self.my_account_button.setFixedSize(200, 50)
        self.my_account_button.clicked.connect(self.show_my_account)
        self.my_account_layout.addWidget(self.my_account_button, alignment=Qt.AlignCenter)

        self.logout_button = QPushButton('Log Out', self)
        self.logout_button.setFixedSize(200, 50)
        self.logout_button.setStyleSheet("font-size: 20px; font-weight: bold; font-style: italic;"
                                         "background-color: red; color:white")
        #self.logout_button.clicked.connect(self.logout)
        self.my_account_layout.addWidget(self.logout_button, alignment=Qt.AlignCenter)

        # Set layout for "My Account" screen
        self.my_account_widget.setLayout(self.my_account_layout)
        self.setCentralWidget(self.my_account_widget)

    def show_my_account(self):
        # Pass main_window (self) and customer_id to the UserAccount class
        user_account = UserAccount(self, self.customer_id)
        user_account.show_my_account()

    def init_menu_screen(self):
        # Pass main_window (self) to the Menu class and call its init_menu_screen method
        self.menu = Menu(self)
        self.menu.init_menu_screen()

    def init_checkout_screen(self):
        # Pass the pizza_spinboxes and sidedish_spinboxes to the Checkout class
        checkout = Checkout(self, self.menu.pizza_spinboxes, self.menu.sidedish_spinboxes)
        checkout.init_checkout_screen()


    def logout(self):
        # Handle logout button click (return to log in screen)
        self.init_login_screen()

    def clear_screen(self):
        # Helper function to clear the screen
        widget = self.centralWidget()
        if widget:
            widget.deleteLater()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PizzaOrderingApp()
    window.show()
    sys.exit(app.exec_())
