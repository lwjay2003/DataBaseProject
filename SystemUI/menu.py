from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QGridLayout, QLabel, QSpinBox, QPushButton
from PyQt5.QtCore import Qt
from database import PizzaDatabase  # Import your PizzaDatabase class


class Menu:
    def __init__(self, main_window):
        self.main_window = main_window  # Reference to the main window to interact with
        self.pizza_spinboxes = {}
        self.sidedish_spinboxes = {}
        self.database = PizzaDatabase()  # Initialize the database class to query pizza and side dishes

    def init_menu_screen(self):
        # Clear the current screen
        self.main_window.clear_screen()

        # Create a tab widget with two tabs: Pizza and Side Dishes
        self.menu_widget = QWidget()
        self.menu_layout = QVBoxLayout()

        self.tab_widget = QTabWidget()

        # Fetch menu items (pizzas and side dishes) from the database
        menu_items = self.database.get_menu_items()
        pizzas = menu_items.get('pizzas', [])  # List of pizzas
        sidedishes = menu_items.get('sidedishes', [])  # List of side dishes

        if not pizzas and not sidedishes:
            # Handle case where no pizzas or side dishes are available
            error_label = QLabel("No menu items available.")
            self.menu_layout.addWidget(error_label)
        else:
            # Pizza Tab
            self.pizza_tab = QWidget()
            self.pizza_layout = QGridLayout()

            # Create pizza labels and spinboxes
            for i, pizza in enumerate(pizzas):
                pizza_label = QLabel(pizza['name'])
                pizza_label.setFixedWidth(200)
                pizza_label.setStyleSheet("font-size: 24px; font-weight: bold; font-style: italic;"
                                          "border-radius: 10px; "
                                          "background-color: red;"
                                          "color:white;")
                pizza_spinbox = QSpinBox()  # User can select quantity
                pizza_spinbox.setFixedSize(50, 50)
                pizza_spinbox.setRange(0, 10)
                self.pizza_layout.addWidget(pizza_label, i, 0)
                self.pizza_layout.addWidget(pizza_spinbox, i, 1)
                self.pizza_spinboxes[pizza['id']] = pizza_spinbox  # Use pizza id as the key

            self.pizza_tab.setLayout(self.pizza_layout)
            self.tab_widget.addTab(self.pizza_tab, "Pizza")
            self.tab_widget.setStyleSheet("font-size: 16px; font-weight: bold; font-style: italic;")

            # Side Dishes Tab
            self.sidedish_tab = QWidget()
            self.sidedish_layout = QGridLayout()

            # Create side dish labels and spinboxes
            for i, dish in enumerate(sidedishes):
                dish_label = QLabel(dish['name'])
                dish_label.setFixedWidth(200)
                dish_label.setStyleSheet("font-size: 24px; font-weight: bold; font-style: italic;"
                                         "border-radius: 10px; "
                                         "background-color: red;"
                                         "color:white;")
                dish_spinbox = QSpinBox()  # User can select quantity
                dish_spinbox.setFixedSize(50, 50)
                dish_spinbox.setRange(0, 20)
                self.sidedish_layout.addWidget(dish_label, i, 0)
                self.sidedish_layout.addWidget(dish_spinbox, i, 1)
                self.sidedish_spinboxes[dish['id']] = dish_spinbox  # Use side dish id as the key

            self.sidedish_tab.setLayout(self.sidedish_layout)
            self.tab_widget.addTab(self.sidedish_tab, "Side Dishes")

            # Add the tab widget to the menu layout
            self.menu_layout.addWidget(self.tab_widget)

        # Checkout button
        self.checkout_button = QPushButton('Checkout')
        self.checkout_button.setStyleSheet("font-size: 16px; font: bold; font-style: italic;"
                                           "color: white;"
                                           "background-color: grey")
        self.checkout_button.setFixedSize(100, 50)

        # Connect to the checkout screen
        self.checkout_button.clicked.connect(self.main_window.init_checkout_screen)
        self.menu_layout.addWidget(self.checkout_button, alignment=Qt.AlignCenter)

        self.menu_widget.setLayout(self.menu_layout)
        self.main_window.setCentralWidget(self.menu_widget)
