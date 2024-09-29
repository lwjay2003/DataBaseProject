CREATE TABLE pizza(
	pizza_id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE ingredient(
	ingredient_id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(50) NOT NULL UNIQUE,
	category ENUM('VEGETABLE', 'MEAT', 'DAIRY'),
	price FLOAT NOT NULL
);

CREATE TABLE pizza_to_ingredient(
	pizza_id INT NOT NULL,
	ingredient_id INT NOT NULL,
	FOREIGN KEY(ppizza_id) REFERENCES pizza(pizza_id),
	FOREIGN KEY(ingredient_id) REFERENCES ingredient(ingredient_id)
);

CREATE TABLE sidedish(
	sidedish_id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(50) NOT NULL UNIQUE,
	price FLOAT NOT NULL
);

CREATE TABLE customer(
	customer_id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(50) NOT NULL,
    gender ENUM('MALE', 'FEMALE'),
    birthday date,
    phone VARCHAR(20) NOT NULL,
	address VARCHAR(255) NOT NULL,
	postcode VARCHAR(6) NOT NULL,
	accumulation INT DEFAULT 0
);

CREATE TABLE order_info(
	order_id INT PRIMARY KEY AUTO_INCREMENT,
	customer_id INT NOT NULL,
	time DATETIME,
	FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);

CREATE TABLE delivery_person(
	delivery_person_id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(50) NOT NULL,
	postcode VARCHAR(6) NOT NULL,
	time DATETIME
);

CREATE TABLE order_to_pizza(
	order_id INT NOT NULL,
	pizza_id INT NOT NULL,
	FOREIGN KEY(order_id) REFERENCES order_info(order_id),
	FOREIGN KEY(pizza_id) REFERENCES pizza(pizza_id)
);

CREATE TABLE order_to_side_dish(
	order_id INT NOT NULL,
	sidedish_id INT NOT NULL,
	FOREIGN KEY(order_id) REFERENCES order_info(order_id),
	FOREIGN KEY(sidedish_id) REFERENCES sidedish(sidedish_id)
);

CREATE TABLE coupon(
	coupon_id INT PRIMARY KEY AUTO_INCREMENT
);