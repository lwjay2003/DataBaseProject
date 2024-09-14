# Independent Pizza Ordering System

## Project Description

In response to recent EU regulations that have banned centralized take-away ordering services for pizza restaurants, each restaurant in Europe is now required to operate its own independent pizza ordering system. This project aims to develop a comprehensive software solution for pizza restaurants, enabling them to manage their own ordering, processing, and delivery operations effectively.

The system is designed using a modular approach, with a clear separation of concerns between **models**, **controllers**, and **views**. This architecture ensures the system is **scalable**, **maintainable**, and **easy to extend**, adhering to software engineering best practices. While some foundational work may already exist in the controller layer from similar projects, this system focuses on building and integrating the **model layer**, expanding functionality to meet the specific needs of a modern pizza restaurant.

## Features

### 1. Menu Presentation

The system provides a dynamic, user-friendly menu that includes:

- **Pizza Listings**: A list of all available pizzas with detailed information about each one.
- **Ingredients**: A display of all ingredients used for each pizza.
- **Price Calculation**: Prices are calculated based on the sum of ingredient costs, a 40% profit margin, and 9% VAT.
- **Dietary Information**: Clear indications of vegetarian and vegan options based on the ingredients.
- **Additional Items**: Drinks and desserts listed as part of the menu.

**Requirements**:
- At least **10 distinct pizzas** with at least **10 different ingredients**.
- At least **4 drinks** and **2 desserts**.

This menu serves as the first point of interaction between the customer and the system, ensuring ease of use while dynamically calculating and presenting pricing and dietary information.

### 2. Order Processing

The system manages the full lifecycle of orders, including:

- **Order Placement**: Customers can place orders for pizzas, drinks, and desserts, with a minimum of one pizza per order.
- **Customer Information Management**: Essential customer information is stored, including name, gender, birthdate, phone number, and address, facilitating order confirmation and delivery.
- **Customer Accounts and Discounts**:
    - A simple login system for customers.
    - Automatic **10% discount** after **10 pizzas** are ordered.
    - Validation and redemption of discount codes, usable only once.
    - **Free pizza and drink** for customers on their birthday.
- **Order Confirmation**: Customers receive a confirmation with order details and estimated delivery time.
- **Restaurant Monitoring**: A real-time display for staff shows pizzas ordered but not yet dispatched.
- **Earnings Report**: A monthly earnings report with filtering options (postal code, city, customer gender, age).

### 3. Order Delivery

Delivery management features include:

- **Delivery Status**: Customers can check the status of their order and the estimated delivery time.
- **Order Cancellation**: Orders can be canceled within **5 minutes** of being placed.
- **Delivery Personnel Management**:
    - Delivery personnel are assigned to specific postal code areas.
    - Delivery persons are unavailable for further deliveries for **30 minutes** after initiating a delivery.
    - Multiple delivery persons can be assigned to the same postal code if needed.
    - Orders from the same postal code that are placed within 5 minutes can be grouped into a single delivery.

## Software Requirements

This project requires the following technical features and considerations:

- A **scalable** and **modular architecture**, ensuring separation of concerns between the model, controller, and view layers.
- Dynamic **price calculations** based on ingredient costs, profit margins, and tax rates.
- Robust **customer and order management**, including account logins, discounts, and delivery monitoring.
- **Real-time order tracking** and delivery management system for both customers and restaurant staff.
- **Reporting tools** for earnings and performance tracking based on region and customer demographics.

By implementing this system, each pizza restaurant can comply with EU regulations while providing a high-quality, user-friendly ordering experience for their customers.

## Project Member
- student ID: i6336504 (Siyao Zhou)
- student ID: i6314340 (Wenjie Liao)
