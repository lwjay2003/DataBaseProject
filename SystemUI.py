import sys

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
        pixmap = QPixmap('/Users/liaowenjie/PycharmProjects/DataBaseProject/Iconarchive-Fat-Sugar-Food-Pizza.512.png')
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

    def login(self):
        # Handle user login logic (validate against your database for later)
        self.username = self.username_input.text()
        if self.username:
            # Proceed to pizza selection screen after login
            self.init_my_account_screen()

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
        #self.my_account_button.clicked.connect(self.show_my_account)
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

    def init_menu_screen(self):
        # Clear current screen
        self.clear_screen()

        # Create a tab widget with two tabs: Pizza and Side Dishes
        self.menu_widget = QWidget()
        self.menu_layout = QVBoxLayout()


        self.tab_widget = QTabWidget()

        # Pizza Tab
        self.pizza_tab = QWidget()
        self.pizza_layout = QGridLayout()
        self.pizza_spinboxes = {}

        pizzas = ["Pepperoni", "Meat Lovers", "Ham", "Salami", "BBQ Chicken", "Hawaii",
                  "New York", "Margaritha", "Black Truffle", "4 Cheese", "Funghi"]



        for i, pizza in enumerate(pizzas):
            pizza_label = QLabel(pizza)
            pizza_label.setFixedWidth(200)
            pizza_label.setStyleSheet("font-size: 24px; font-weight: bold; font-style: italic;"
                                      "border-radius: 10px; "
                                      "background-color: red;"
                                      "width: auto;"
                                      "color:white"
                                      )
            pizza_spinbox = QSpinBox()  # User can select quantity
            pizza_spinbox.setFixedSize(50, 50)
            pizza_spinbox.setRange(0, 10)
            self.pizza_layout.addWidget(pizza_label, i, 0)
            self.pizza_layout.addWidget(pizza_spinbox, i, 1)
            self.pizza_spinboxes[pizza] = pizza_spinbox

        self.pizza_tab.setLayout(self.pizza_layout)
        self.tab_widget.addTab(self.pizza_tab, "Pizza")
        self.tab_widget.setStyleSheet("font-size: 16px; font-weight: bold; font-style: italic;")

        # Side Dishes Tab
        self.sidedish_tab = QWidget()
        self.sidedish_layout = QGridLayout()
        self.sidedish_spinboxes = {}

        sidedishes = ["Garlic Bread", "Caesar Salad", "Chicken Wings", "Tiramisu", "Apple Pie",
                      "Cola", "Sprite", "Lemonade", "Orange Juice"]


        for i, dish in enumerate(sidedishes):
            dish_label = QLabel(dish)
            dish_label.setFixedWidth(200)
            dish_label.setStyleSheet("font-size: 24px; font-weight: bold; font-style: italic;"
                                     "border-radius: 10px; "
                                     "background-color: red;"
                                     "width: auto;"
                                     "color:white"
                                     )
            dish_spinbox = QSpinBox()  # User can select quantity
            dish_spinbox.setFixedSize(50, 50)
            dish_spinbox.setRange(0, 20)
            self.sidedish_layout.addWidget(dish_label, i, 0)
            self.sidedish_layout.addWidget(dish_spinbox, i, 1)

        self.sidedish_tab.setLayout(self.sidedish_layout)
        self.tab_widget.addTab(self.sidedish_tab, "Side Dishes")
        self.tab_widget.setStyleSheet("font-size: 16px; font-weight: bold; font-style: italic;")

        # Add the tab widget to the menu layout
        self.menu_layout.addWidget(self.tab_widget)

        # Checkout button
        self.checkout_button = QPushButton('Checkout')
        self.checkout_button.setStyleSheet("font-size: 16px; font: bold; font-style: italic;"
                                           "color: white;"
                                           "background-color: grey")
        self.checkout_button.setFixedSize(100, 50)

        self.checkout_button.clicked.connect(self.init_checkout_screen)
        self.menu_layout.addWidget(self.checkout_button, alignment=Qt.AlignCenter)

        self.menu_widget.setLayout(self.menu_layout)
        self.setCentralWidget(self.menu_widget)

    def init_checkout_screen(self):
        self.clear_screen()

        self.checkout_widget = QWidget()
        self.checkout_layout = QVBoxLayout()

        self.order_table = QTableWidget()
        self.order_table.setColumnCount(3)
        self.order_table.setHorizontalHeaderLabels(['Item', 'Quantity', 'Price'])
        self.order_table.horizontalHeader().setStretchLastSection(True)

        items_ordered = []
        total_price = 0

        # Calculate total price and add ordered pizzas
        pizza_prices = {"Pepperoni": 10, "Meat Lovers": 12, "Ham": 8, "Salami": 9, "BBQ Chicken": 11,
                        "Hawaii": 9, "New York": 10, "Margaritha": 8, "Black Truffle": 14, "4 Cheese": 12, "Funghi": 10}

        for pizza, spinbox in self.pizza_spinboxes.items():
            quantity = spinbox.value()
            if quantity > 0:
                price = pizza_prices[pizza] * quantity
                total_price += price
                items_ordered.append((pizza, quantity, price))

        # Add ordered side dishes
        sidedish_prices = {"Garlic Bread": 3, "Caesar Salad": 4, "Chicken Wings": 6, "Tiramisu": 5, "Apple Pie": 4,
                           "Cola": 2, "Sprite": 2, "Lemonade": 2, "Orange Juice": 2}

        for dish, spinbox in self.sidedish_spinboxes.items():
            quantity = spinbox.value()
            if quantity > 0:
                price = sidedish_prices[dish] * quantity
                total_price += price
                items_ordered.append((dish, quantity, price))

        self.order_table.setRowCount(len(items_ordered))

        for i, (item, quantity, price) in enumerate(items_ordered):
            self.order_table.setItem(i, 0, QTableWidgetItem(item))
            self.order_table.setItem(i, 1, QTableWidgetItem(str(quantity)))
            self.order_table.setItem(i, 2, QTableWidgetItem(f"${price:.2f}"))

        self.checkout_layout.addWidget(self.order_table)

        self.total_price_label = QLabel(f"Total Price: ${total_price:.2f}")
        self.total_price_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.checkout_layout.addWidget(self.total_price_label, alignment=Qt.AlignRight)

        self.place_order_button = QPushButton('Place Order')
        self.place_order_button.setFixedSize(200, 50)
        self.place_order_button.setStyleSheet("font-size: 16px; color: white; background-color: green")
        self.place_order_button.clicked.connect(self.place_order)
        self.checkout_layout.addWidget(self.place_order_button, alignment=Qt.AlignCenter)

        self.checkout_widget.setLayout(self.checkout_layout)
        self.setCentralWidget(self.checkout_widget)

    def place_order(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText("Thank you for your order! Your pizza will be ready soon.")
        msg_box.setWindowTitle("Order Confirmation")
        msg_box.exec_()

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
