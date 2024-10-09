from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QPushButton, QMessageBox
from database import PizzaDatabase


class Checkout:
    def __init__(self, main_window, pizza_spinboxes, sidedish_spinboxes):
        self.main_window = main_window  # Reference to main window to interact with
        self.pizza_spinboxes = pizza_spinboxes  # Store pizza spinbox data
        self.sidedish_spinboxes = sidedish_spinboxes  # Store side dish spinbox data
        self.database = PizzaDatabase()  # Initialize PizzaDatabase to fetch pizza and ingredient prices

    def init_checkout_screen(self):
        self.main_window.clear_screen()

        self.checkout_widget = QWidget()
        self.checkout_layout = QVBoxLayout()

        self.order_table = QTableWidget()
        self.order_table.setColumnCount(4)  # Now 4 columns: Item, Quantity, Price, VAT
        self.order_table.setHorizontalHeaderLabels(['Item', 'Quantity', 'Price (with VAT)', 'VAT Amount'])
        self.order_table.horizontalHeader().setStretchLastSection(True)

        items_ordered = []
        total_price = 0
        total_vat = 0  # Keep track of total VAT

        # Fetch dynamic pizza prices from the database
        for pizza_id, spinbox in self.pizza_spinboxes.items():
            quantity = spinbox.value()
            if quantity > 0:
                # Fetch pizza details and calculate the total price based on ingredients
                pizza = self.database.get_pizza(pizza_id)
                base_price, vat_amount, final_price = self.calculate_pizza_price(pizza_id)  # Get price with VAT breakdown
                price = final_price * quantity
                vat = vat_amount * quantity
                total_price += price
                total_vat += vat
                items_ordered.append((pizza['name'], quantity, price, vat))  # Include VAT amount in the tuple

        # Fetch side dish prices from the database
        for dish_id, spinbox in self.sidedish_spinboxes.items():
            quantity = spinbox.value()
            if quantity > 0:
                # Fetch side dish details from the database
                side_dish = self.database.get_side_dish(dish_id)
                base_price = side_dish['price']
                vat_amount = base_price * 0.09  # VAT for side dishes is 9%
                final_price = base_price + vat_amount
                price = final_price * quantity
                vat = vat_amount * quantity
                total_price += price
                total_vat += vat
                items_ordered.append((side_dish['name'], quantity, price, vat))  # Include VAT for side dishes

        # Set up the order table
        self.order_table.setRowCount(len(items_ordered))

        # Fill the table with items ordered
        for i, (item, quantity, price, vat) in enumerate(items_ordered):
            self.order_table.setItem(i, 0, QTableWidgetItem(item))
            self.order_table.setItem(i, 1, QTableWidgetItem(str(quantity)))
            self.order_table.setItem(i, 2, QTableWidgetItem(f"${price:.2f}"))
            self.order_table.setItem(i, 3, QTableWidgetItem(f"${vat:.2f}"))  # Display VAT amount

        self.checkout_layout.addWidget(self.order_table)

        # Display total price and VAT
        self.total_price_label = QLabel(f"Total Price (with VAT): ${total_price:.2f}")
        self.total_vat_label = QLabel(f"Total VAT Amount: ${total_vat:.2f}")
        self.total_price_label.setStyleSheet("font-size: 24px; color:white; background-color:black;font-weight: bold;")
        self.total_vat_label.setStyleSheet("font-size: 18px; color:white; background-color:black;font-weight: bold;")
        self.checkout_layout.addWidget(self.total_vat_label, alignment=Qt.AlignRight)
        self.checkout_layout.addWidget(self.total_price_label, alignment=Qt.AlignRight)

        # Place order button
        self.place_order_button = QPushButton('Place Order')
        self.place_order_button.setFixedSize(200, 50)
        self.place_order_button.setStyleSheet("font-size: 16px; color: white; background-color: green")
        self.place_order_button.clicked.connect(self.place_order)
        self.checkout_layout.addWidget(self.place_order_button, alignment=Qt.AlignCenter)

        self.checkout_widget.setLayout(self.checkout_layout)
        self.main_window.setCentralWidget(self.checkout_widget)

    def calculate_pizza_price(self, pizza_id):
        """
        Calculate the total price of a pizza based on its ingredients,
        a 40% profit margin, and a 9% VAT. Return base price, VAT amount, and final price.
        """
        # Fetch the pizza details, including its ingredients
        pizza = self.database.get_pizza(pizza_id)
        ingredient_cost = 0

        # Calculate the total ingredient cost
        for ingredient_id in pizza['ingredients']:
            ingredient = self.database.get_ingredient(ingredient_id)
            ingredient_cost += ingredient['price']

        # Add 40% profit margin to the ingredient
        price_with_profit = ingredient_cost * 1.40

        # Calculate 9% VAT
        vat_amount = price_with_profit * 0.09
        final_price = price_with_profit + vat_amount

        return price_with_profit, vat_amount, final_price

    @staticmethod
    def place_order():
        # Show confirmation message
        print("the button is clicked")
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText("Thank you for your order! Your pizza will be ready soon.")
        msg_box.setWindowTitle("Order Confirmation")
        msg_box.exec_()
