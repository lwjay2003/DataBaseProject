-- Non-Vegetarian Pizza
INSERT INTO pizza(name) values ('pepperoni');
INSERT INTO pizza(name) values ('meat lovers');
INSERT INTO pizza(name) values ('ham');
INSERT INTO pizza(name) values ('salami');
INSERT INTO pizza(name) values ('bbq chicken');
INSERT INTO pizza(name) values ('new york');

-- Vegetarian Pizza
INSERT INTO pizza(name) values ('hawaii');
INSERT INTO pizza(name) values ('margaritha');
INSERT INTO pizza(name) values ('black truffle');
INSERT INTO pizza(name) values ('4 cheese');

-- Vegan Pizza
INSERT INTO pizza(name) values ('funghi');

-- Insert all unique ingredients
INSERT INTO ingredient(name, category, price) 
VALUES 
  ('Mozzarella', 'DAIRY', 1.25),
  ('Pepperoni', 'MEAT', 1.50),
  ('Tomato Sauce', 'VEGETABLE', 0.50),
  ('Ham', 'MEAT', 1.30),
  ('Sausage', 'MEAT', 1.40),
  ('Bacon', 'MEAT', 1.60),
  ('Chicken', 'MEAT', 1.60),
  ('Red Onion', 'VEGETABLE', 0.30),
  ('Pineapple', 'VEGETABLE', 0.80),
  ('Oregano', 'VEGETABLE', 0.20),
  ('Fresh Basil', 'VEGETABLE', 0.20),
  ('Mushrooms', 'VEGETABLE', 0.90),
  ('Cheddar', 'DAIRY', 1.50),
  ('Parmesan', 'DAIRY', 1.40),
  ('Ricotta', 'DAIRY', 1.30),
  ('Bell Pepper', 'VEGETABLE', 0.40);
  
-- Pepperoni Pizza (id = 1)
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (1, 1); -- Mozzarella
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (1, 2); -- Pepperoni
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (1, 3); -- Tomato Sauce

-- Meat Lovers Pizza (id = 2)
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (2, 1); -- Mozzarella
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (2, 2); -- Pepperoni
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (2, 4); -- Ham
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (2, 5); -- Sausage
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (2, 6); -- Bacon
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (2, 3); -- Tomato Sauce

-- Ham Pizza (id = 3)
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (3, 1); -- Mozzarella
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (3, 4); -- Ham
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (3, 3); -- Tomato Sauce

-- Salami Pizza (id = 4)
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (4, 1); -- Mozzarella
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (4, 2); -- Pepperoni (as a replacement for Salami)
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (4, 3); -- Tomato Sauce

-- BBQ Chicken Pizza (id = 5)
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (5, 1); -- Mozzarella
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (5, 7); -- Chicken
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (5, 8); -- Red Onion
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (5, 3); -- Tomato Sauce

-- Hawaii Pizza (id = 6)
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (6, 1); -- Mozzarella
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (6, 4); -- Ham
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (6, 9); -- Pineapple
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (6, 3); -- Tomato Sauce

-- New York Pizza (id = 7)
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (7, 1); -- Mozzarella
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (7, 2); -- Pepperoni
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (7, 3); -- Tomato Sauce
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (7, 10); -- Oregano

-- Margaritha Pizza (id = 8)
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (8, 1); -- Mozzarella
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (8, 3); -- Tomato Sauce
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (8, 11); -- Fresh Basil

-- Black Truffle Pizza (id = 9)
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (9, 1); -- Mozzarella
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (9, 12); -- Mushrooms
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (9, 3); -- Tomato Sauce

-- 4 Cheese Pizza (id = 10)
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (10, 1); -- Mozzarella
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (10, 13); -- Cheddar
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (10, 14); -- Parmesan
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (10, 15); -- Ricotta
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (10, 3); -- Tomato Sauce

-- Funghi Pizza (id = 11, Vegan)
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (11, 3); -- Tomato Sauce
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (11, 12); -- Mushrooms
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (11, 16); -- Bell Pepper
INSERT INTO pizza_to_ingredient(pizza_id, ingredient_id) VALUES (11, 8);  -- Red Onion

-- Side dish
INSERT INTO sidedish(name, price) values ('garlic bread', 3.50);
INSERT INTO sidedish(name, price) values ('chicken wings', 6.00);
INSERT INTO sidedish(name, price) values ('tiramisu', 5.50);
INSERT INTO sidedish(name, price) values ('apple pie', 4.50);
INSERT INTO sidedish(name, price) values ('cola', 2.50);
INSERT INTO sidedish(name, price) values ('sprite', 2.50);
INSERT INTO sidedish(name, price) values ('lemonade', 3.00);
INSERT INTO sidedish(name, price) values ('orange juice', 3.25);

-- Customer
INSERT INTO customer(name, gender, birthday, phone, address, postcode, accumulation) 
VALUES 
('Anna van Dijk', 'FEMALE', '1990-06-15', '0623456789', 'Sint Annalaan 20', '6214AA', 0),    
('Evi Smeets', 'FEMALE', '2000-02-09', '0656789012', 'Brusselsestraat 3', '6211PB', 10),     
('Hugo Martens', 'MALE', '1996-03-25', '0689012345', 'Wycker Grachtstraat 102', '6221CT', 10),
('Isabel Maas', 'FEMALE', '1994-05-11', '0690123456', 'Maastrichter Heidenstraat 28', '6211HV', 0), 
('Joris Kuipers', 'MALE', '1983-12-04', '0601234567', 'Stationsstraat 88', '6221BR', 9);

-- Deliveryman
INSERT INTO delivery_person(name, postcode) VALUES ('Tom', '6214AA');    
INSERT INTO delivery_person(name, postcode) VALUES ('Kurt', '6221PB');   
INSERT INTO delivery_person(name, postcode) VALUES ('Albert', '6221CT'); 
INSERT INTO delivery_person(name, postcode) VALUES ('Sven', '6211HV');   
INSERT INTO delivery_person(name, postcode) VALUES ('Jasper', '6221BR');









