-- MySQL dump 10.13  Distrib 9.0.1, for macos13.6 (arm64)
--
-- Host: localhost    Database: pizza_ordering
-- ------------------------------------------------------
-- Server version	8.0.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `coupon`
--

DROP TABLE IF EXISTS `coupon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coupon` (
  `coupon_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `discount_percentage` float NOT NULL DEFAULT '0.1',
  PRIMARY KEY (`coupon_id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `coupon_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coupon`
--

LOCK TABLES `coupon` WRITE;
/*!40000 ALTER TABLE `coupon` DISABLE KEYS */;
INSERT INTO `coupon` VALUES (3,1,0.1);
/*!40000 ALTER TABLE `coupon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `customer_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `gender` enum('MALE','FEMALE') DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `phone` varchar(20) NOT NULL,
  `address` varchar(255) NOT NULL,
  `postcode` varchar(6) NOT NULL,
  `accumulation` int DEFAULT '0',
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (1,'Anna van Dijk','FEMALE','1990-06-15','0623456789','Sint Annalaan 20','6214AA',0),(2,'Evi Smeets','FEMALE','2000-02-09','0656789012','Brusselsestraat 3','6211PB',11),(3,'Hugo Martens','MALE','1996-03-25','0689012345','Wycker Grachtstraat 102','6221CT',10),(4,'Isabel Maas','FEMALE','1994-05-11','0690123456','Maastrichter Heidenstraat 28','6211HV',0),(5,'Joris Kuipers','MALE','1983-12-04','0601234567','Stationsstraat 88','6221BR',9);
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `delivery_person`
--

DROP TABLE IF EXISTS `delivery_person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `delivery_person` (
  `delivery_person_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `postcode` varchar(6) NOT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`delivery_person_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `delivery_person`
--

LOCK TABLES `delivery_person` WRITE;
/*!40000 ALTER TABLE `delivery_person` DISABLE KEYS */;
INSERT INTO `delivery_person` VALUES (1,'Tom','6214AA','2024-10-06 11:09:55'),(2,'Kurt','6211PB',NULL),(3,'Albert','6221CT',NULL),(4,'Sven','6211HV',NULL),(5,'Jasper','6221BR',NULL);
/*!40000 ALTER TABLE `delivery_person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingredient`
--

DROP TABLE IF EXISTS `ingredient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingredient` (
  `ingredient_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `category` enum('VEGETABLE','MEAT','DAIRY') DEFAULT NULL,
  `price` float NOT NULL,
  PRIMARY KEY (`ingredient_id`),
  UNIQUE KEY `unique_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredient`
--

LOCK TABLES `ingredient` WRITE;
/*!40000 ALTER TABLE `ingredient` DISABLE KEYS */;
INSERT INTO `ingredient` VALUES (1,'Mozzarella','DAIRY',1.25),(2,'Pepperoni','MEAT',1.5),(3,'Tomato Sauce','VEGETABLE',0.5),(4,'Ham','MEAT',1.3),(5,'Sausage','MEAT',1.4),(6,'Bacon','MEAT',1.6),(7,'Chicken','MEAT',1.6),(8,'Red Onion','VEGETABLE',0.3),(9,'Pineapple','VEGETABLE',0.8),(10,'Oregano','VEGETABLE',0.2),(11,'Fresh Basil','VEGETABLE',0.2),(12,'Mushrooms','VEGETABLE',0.9),(13,'Cheddar','DAIRY',1.5),(14,'Parmesan','DAIRY',1.4),(15,'Ricotta','DAIRY',1.3),(16,'Bell Pepper','VEGETABLE',0.4),(17,'Pizza Dough','VEGETABLE',3);
/*!40000 ALTER TABLE `ingredient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_info`
--

DROP TABLE IF EXISTS `order_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_info` (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `time` datetime DEFAULT NULL,
  `delivery_person_id` int DEFAULT NULL,
  PRIMARY KEY (`order_id`),
  KEY `fk_order_customer_id` (`customer_id`),
  KEY `delivery_person_id` (`delivery_person_id`),
  CONSTRAINT `fk_order_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`),
  CONSTRAINT `order_info_ibfk_1` FOREIGN KEY (`delivery_person_id`) REFERENCES `delivery_person` (`delivery_person_id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_info`
--

LOCK TABLES `order_info` WRITE;
/*!40000 ALTER TABLE `order_info` DISABLE KEYS */;
INSERT INTO `order_info` VALUES (4,1,'2024-10-06 00:10:08',NULL),(7,1,'2024-10-06 00:17:40',NULL),(8,1,'2024-10-06 00:19:10',NULL),(9,1,'2024-10-06 00:19:19',NULL),(11,1,'2024-10-06 00:24:54',1),(13,2,'2024-10-06 09:20:45',NULL),(14,1,'2024-10-06 10:02:11',NULL),(15,1,'2024-10-06 10:02:11',NULL),(16,1,'2024-10-06 10:02:11',NULL),(17,1,'2024-10-06 10:23:42',NULL),(18,1,'2024-10-06 10:23:42',NULL),(19,1,'2024-10-06 10:23:42',NULL),(20,1,'2024-10-06 10:39:44',1),(21,1,'2024-10-06 10:39:44',1),(22,1,'2024-10-06 10:39:44',1);
/*!40000 ALTER TABLE `order_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_to_pizza`
--

DROP TABLE IF EXISTS `order_to_pizza`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_to_pizza` (
  `order_id` int NOT NULL,
  `pizza_id` int NOT NULL,
  KEY `order_to_pizza_relation_1` (`order_id`),
  KEY `order_to_pizza_relation_2` (`pizza_id`),
  CONSTRAINT `order_to_pizza_relation_1` FOREIGN KEY (`order_id`) REFERENCES `order_info` (`order_id`),
  CONSTRAINT `order_to_pizza_relation_2` FOREIGN KEY (`pizza_id`) REFERENCES `pizza` (`pizza_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_to_pizza`
--

LOCK TABLES `order_to_pizza` WRITE;
/*!40000 ALTER TABLE `order_to_pizza` DISABLE KEYS */;
INSERT INTO `order_to_pizza` VALUES (7,1),(7,2),(8,1),(8,2),(9,1),(9,2),(11,1),(11,2),(13,5);
/*!40000 ALTER TABLE `order_to_pizza` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_to_sidedish`
--

DROP TABLE IF EXISTS `order_to_sidedish`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_to_sidedish` (
  `order_id` int NOT NULL,
  `sidedish_id` int NOT NULL,
  KEY `order_to_sidedish_relation_1` (`order_id`),
  KEY `order_to_sidedish_relation_2` (`sidedish_id`),
  CONSTRAINT `order_to_sidedish_relation_1` FOREIGN KEY (`order_id`) REFERENCES `order_info` (`order_id`),
  CONSTRAINT `order_to_sidedish_relation_2` FOREIGN KEY (`sidedish_id`) REFERENCES `sidedish` (`sidedish_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_to_sidedish`
--

LOCK TABLES `order_to_sidedish` WRITE;
/*!40000 ALTER TABLE `order_to_sidedish` DISABLE KEYS */;
INSERT INTO `order_to_sidedish` VALUES (7,1),(8,1),(9,1),(11,1),(13,2);
/*!40000 ALTER TABLE `order_to_sidedish` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pizza`
--

DROP TABLE IF EXISTS `pizza`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pizza` (
  `pizza_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`pizza_id`),
  UNIQUE KEY `UNIQUE` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pizza`
--

LOCK TABLES `pizza` WRITE;
/*!40000 ALTER TABLE `pizza` DISABLE KEYS */;
INSERT INTO `pizza` VALUES (10,'4 cheese'),(5,'bbq chicken'),(9,'black truffle'),(11,'funghi'),(3,'ham'),(6,'hawaii'),(8,'margaritha'),(2,'meat lovers'),(7,'new york'),(1,'pepperoni'),(4,'salami');
/*!40000 ALTER TABLE `pizza` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pizza_to_ingredient`
--

DROP TABLE IF EXISTS `pizza_to_ingredient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pizza_to_ingredient` (
  `pizza_id` int NOT NULL,
  `ingredient_id` int NOT NULL,
  UNIQUE KEY `unique_pizza_ingredient` (`pizza_id`,`ingredient_id`),
  KEY `foreign_ingredient` (`ingredient_id`),
  CONSTRAINT `foreign_ingredient` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredient` (`ingredient_id`),
  CONSTRAINT `foreign_pizza` FOREIGN KEY (`pizza_id`) REFERENCES `pizza` (`pizza_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pizza_to_ingredient`
--

LOCK TABLES `pizza_to_ingredient` WRITE;
/*!40000 ALTER TABLE `pizza_to_ingredient` DISABLE KEYS */;
INSERT INTO `pizza_to_ingredient` VALUES (1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(1,2),(2,2),(4,2),(7,2),(1,3),(2,3),(3,3),(4,3),(5,3),(6,3),(7,3),(8,3),(9,3),(10,3),(11,3),(2,4),(3,4),(6,4),(2,5),(2,6),(5,7),(5,8),(11,8),(6,9),(7,10),(8,11),(9,12),(11,12),(10,13),(10,14),(10,15),(11,16),(1,17),(2,17),(3,17),(4,17),(5,17),(6,17),(7,17),(8,17),(9,17),(10,17),(11,17);
/*!40000 ALTER TABLE `pizza_to_ingredient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sidedish`
--

DROP TABLE IF EXISTS `sidedish`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sidedish` (
  `sidedish_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `price` float NOT NULL,
  PRIMARY KEY (`sidedish_id`),
  UNIQUE KEY `Unique` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sidedish`
--

LOCK TABLES `sidedish` WRITE;
/*!40000 ALTER TABLE `sidedish` DISABLE KEYS */;
INSERT INTO `sidedish` VALUES (1,'garlic bread',3.5),(2,'caesar salad',5.25),(3,'chicken wings',6),(4,'tiramisu',5.5),(5,'apple pie',4.5),(6,'cola',2.5),(7,'sprite',2.5),(8,'lemonade',3),(9,'orange juice',3.25);
/*!40000 ALTER TABLE `sidedish` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `customer_id` int DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `customer_id` (`customer_id`),
  CONSTRAINT `fk_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'anna','password1',1),(2,'evi','password2',2),(3,'hugo','password3',3),(4,'isabel','password4',4),(5,'joris','password5',5);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-09 20:09:27
