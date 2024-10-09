from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QSpinBox, QTabWidget, QPushButton
from database import PizzaDatabase  # Import PizzaDatabase for fetching pizzas and ingredients


class Menu:
    def __init__(self, main_window):
        self.main_window = main_window  # Reference to main window to interact with
        self.pizza_spinboxes = {}  # To store spinbox widgets for pizzas
        self.sidedish_spinboxes = {}  # To store spinbox widgets for side dishes
        self.database = PizzaDatabase()  # Initialize PizzaDatabase to fetch menu items

    def init_menu_screen(self):
        self.main_window.clear_screen()

        self.menu_widget = QWidget()
        self.menu_layout = QVBoxLayout()

        self.tab_widget = QTabWidget()

        # Fetch menu items (pizzas and side dishes) from the database
        menu_items = self.database.get_menu_items()
        pizzas = menu_items.get('pizzas', [])  # List of pizzas
        sidedishes = menu_items.get('sidedishes', [])  # List of side dishes

        # Pizza Tab
        self.pizza_tab = QWidget()
        self.pizza_layout = QGridLayout()

        # Create pizza labels and spinboxes with ingredients and prices
        for i, pizza in enumerate(pizzas):
            pizza_label = QLabel(self.format_pizza_label(pizza))  # Use helper method to format the label
            pizza_label.setFixedWidth(700)
            pizza_label.setStyleSheet("font-size: 10px; font-weight: bold; font-style: italic;"
                                      "border-radius: 10px; background-color: red; color: white;")

            pizza_spinbox = QSpinBox()  # User can select quantity
            pizza_spinbox.setFixedSize(50, 50)
            pizza_spinbox.setRange(0, 10)

            # Add pizza label and spinbox to the layout
            self.pizza_layout.addWidget(pizza_label, i, 0)
            self.pizza_layout.addWidget(pizza_spinbox, i, 1)
            self.pizza_spinboxes[pizza['id']] = pizza_spinbox  # Store the spinbox with pizza ID as key

        self.pizza_tab.setLayout(self.pizza_layout)
        self.tab_widget.addTab(self.pizza_tab, "Pizza")

        # Side Dishes Tab
        self.sidedish_tab = QWidget()
        self.sidedish_layout = QGridLayout()

        # Create side dish labels and spinboxes with prices
        for i, dish in enumerate(sidedishes):
            dish_label = QLabel(f"{dish['name']} - ${dish['price']:.2f}")
            dish_label.setFixedWidth(400)
            dish_label.setStyleSheet("font-size: 18px; font-weight: bold; font-style: italic;"
                                     "border-radius: 10px; background-color: red; color: white;")

            dish_spinbox = QSpinBox()  # User can select quantity
            dish_spinbox.setFixedSize(50, 50)
            dish_spinbox.setRange(0, 20)

            # Add dish label and spinbox to the layout
            self.sidedish_layout.addWidget(dish_label, i, 0)
            self.sidedish_layout.addWidget(dish_spinbox, i, 1)
            self.sidedish_spinboxes[dish['id']] = dish_spinbox  # Store the spinbox with dish ID as key

        self.sidedish_tab.setLayout(self.sidedish_layout)
        self.tab_widget.addTab(self.sidedish_tab, "Side Dishes")

        # Add the tab widget to the menu layout
        self.menu_layout.addWidget(self.tab_widget)
        self.menu_widget.setLayout(self.menu_layout)
        self.main_window.setCentralWidget(self.menu_widget)

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

    def format_pizza_label(self, pizza):
        """
        Helper method to format the pizza label, including name, ingredients, and price.
        If the pizza is vegan, append a 'Vegan' label.
        """
        # 使用 ingredient_ids 列表获取配料名称
        ingredients = [self.database.get_ingredient(ingredient_id)['name'] for ingredient_id in pizza['ingredients']]

        # 计算价格和是否为素食
        base_price, vat_amount, final_price, is_vegan = self.calculate_pizza_price(pizza['id'])

        # 格式化标签，如果是素食则添加 'Vegan' 标签
        vegan_label = " (Vegan)" if is_vegan else ""
        return f"{pizza['name']} - Ingredients: {', '.join(ingredients)} - Price: ${final_price:.2f} (incl. VAT){vegan_label}"

    def calculate_pizza_price(self, pizza_id):
        """
        Calculate the total price of a pizza based on its ingredients,
        a 40% profit margin, and a 9% VAT. Determine if the pizza is vegan based on its ingredients.
        """
        # 获取披萨详情，包括配料 ID 列表
        pizza = self.database.get_pizza(pizza_id)
        ingredient_cost = 0
        is_vegan = True  # 默认假设披萨是素食的

        # 计算总配料成本并检查所有配料是否为素食
        for ingredient_id in pizza['ingredients']:
            ingredient = self.database.get_ingredient(ingredient_id)
            ingredient_cost += ingredient['price']
            if not ingredient['vegan']:  # 如果任何配料不是素食，则披萨不是素食
                is_vegan = False

        # 添加 40% 利润
        price_with_profit = ingredient_cost * 1.40

        # 计算 9% VAT
        vat_amount = price_with_profit * 0.09
        final_price = price_with_profit + vat_amount

        return price_with_profit, vat_amount, final_price, is_vegan


