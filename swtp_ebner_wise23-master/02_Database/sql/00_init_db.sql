-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Generation Time: Mar 31, 2023 at 02:18 PM
-- Server version: 10.11.2-MariaDB-1:10.11.2+maria~ubu2204
-- PHP Version: 8.1.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `drink_machine`
--
CREATE DATABASE IF NOT EXISTS `drink_machine` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `drink_machine`;

-- --------------------------------------------------------

--
-- Table structure for table `bottle`
--

CREATE TABLE `bottle` (
  `bottleID` int(11) NOT NULL,
  `categoryID` int(11) NOT NULL,
  `name` text NOT NULL,
  `density` decimal(10,3) NOT NULL DEFAULT 1.000,
  `max_capacity` int(11) NOT NULL,
  `alcohol_percentage` decimal(5,2) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `pic_url` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bottleitem`
--

CREATE TABLE `bottleitem` (
  `bottleItemID` int(11) NOT NULL,
  `machineID` int(11) NOT NULL,
  `bottleID` int(11) NOT NULL,
  `position_cm` int(11) NOT NULL,
  `pump_pin` int(11) NOT NULL,
  `led_pin` int(11) NOT NULL,
  `current_capacity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `categoryID` int(11) NOT NULL,
  `parent_categoryID` int(11) DEFAULT NULL,
  `name` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `glass`
--

CREATE TABLE `glass` (
  `glassID` int(11) NOT NULL,
  `amount_ml` int(11) NOT NULL,
  `weight_g` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `machine`
--

CREATE TABLE `machine` (
  `machineID` int(11) NOT NULL,
  `name` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `order`
--

CREATE TABLE `order` (
  `orderID` int(11) NOT NULL,
  `recipeID` int(11) DEFAULT NULL,
  `glassID` int(11) NOT NULL,
  `machineID` int(11) NOT NULL,
  `start_time` datetime NOT NULL,
  `last_update` datetime NOT NULL,
  `status` enum('completed','pending','waiting','failed') NOT NULL,
  `clientID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `orderitem`
--

CREATE TABLE `orderitem` (
  `orderItemID` int(11) NOT NULL,
  `bottleID` int(11) NOT NULL,
  `orderID` int(11) NOT NULL,
  `amount_ml` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `recipe`
--

CREATE TABLE `recipe` (
  `recipeID` int(11) NOT NULL,
  `glassID` int(11) NOT NULL,
  `categoryID` int(11) NOT NULL,
  `name` text NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `rating_value` decimal(3,2) NOT NULL DEFAULT 0.00,
  `rating_number` int(11) NOT NULL DEFAULT 0,
  `pic_url` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `recipeitem`
--

CREATE TABLE `recipeitem` (
  `recipeItemID` int(11) NOT NULL,
  `recipeID` int(11) NOT NULL,
  `categoryID` int(11) NOT NULL,
  `amount_ml` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `userID` int(11) NOT NULL,
  `password` varchar(20) NOT NULL,
  `name` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bottle`
--
ALTER TABLE `bottle`
  ADD PRIMARY KEY (`bottleID`),
  ADD KEY `categoryID` (`categoryID`);

--
-- Indexes for table `bottleitem`
--
ALTER TABLE `bottleitem`
  ADD PRIMARY KEY (`bottleItemID`),
  ADD KEY `bottleID` (`bottleID`),
  ADD KEY `machineID` (`machineID`);

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`categoryID`),
  ADD KEY `parent_categoryID` (`parent_categoryID`);

--
-- Indexes for table `glass`
--
ALTER TABLE `glass`
  ADD PRIMARY KEY (`glassID`);

--
-- Indexes for table `machine`
--
ALTER TABLE `machine`
  ADD PRIMARY KEY (`machineID`);

--
-- Indexes for table `order`
--
ALTER TABLE `order`
  ADD PRIMARY KEY (`orderID`),
  ADD KEY `glassID` (`glassID`),
  ADD KEY `machineID` (`machineID`),
  ADD KEY `recipeID` (`recipeID`);

--
-- Indexes for table `orderitem`
--
ALTER TABLE `orderitem`
  ADD PRIMARY KEY (`orderItemID`),
  ADD KEY `orderID` (`orderID`),
  ADD KEY `bottleID` (`bottleID`);

--
-- Indexes for table `recipe`
--
ALTER TABLE `recipe`
  ADD PRIMARY KEY (`recipeID`),
  ADD KEY `categoryID` (`categoryID`),
  ADD KEY `glassID` (`glassID`);

--
-- Indexes for table `recipeitem`
--
ALTER TABLE `recipeitem`
  ADD PRIMARY KEY (`recipeItemID`),
  ADD KEY `categoryID` (`categoryID`),
  ADD KEY `recipeID` (`recipeID`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`userID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bottle`
--
ALTER TABLE `bottle`
  MODIFY `bottleID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `bottleitem`
--
ALTER TABLE `bottleitem`
  MODIFY `bottleItemID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `categoryID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `glass`
--
ALTER TABLE `glass`
  MODIFY `glassID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `machine`
--
ALTER TABLE `machine`
  MODIFY `machineID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `order`
--
ALTER TABLE `order`
  MODIFY `orderID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `orderitem`
--
ALTER TABLE `orderitem`
  MODIFY `orderItemID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `recipe`
--
ALTER TABLE `recipe`
  MODIFY `recipeID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `recipeitem`
--
ALTER TABLE `recipeitem`
  MODIFY `recipeItemID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `userID` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bottle`
--
ALTER TABLE `bottle`
  ADD CONSTRAINT `Bottles_ibfk_1` FOREIGN KEY (`categoryID`) REFERENCES `category` (`categoryID`);

--
-- Constraints for table `bottleitem`
--
ALTER TABLE `bottleitem`
  ADD CONSTRAINT `bottleItem_ibfk_1` FOREIGN KEY (`machineID`) REFERENCES `machine` (`machineID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `bottleItem_ibfk_2` FOREIGN KEY (`bottleID`) REFERENCES `bottle` (`bottleID`);

--
-- Constraints for table `category`
--
ALTER TABLE `category`
  ADD CONSTRAINT `Categories_ibfk_1` FOREIGN KEY (`parent_categoryID`) REFERENCES `category` (`categoryID`);

--
-- Constraints for table `order`
--
ALTER TABLE `order`
  ADD CONSTRAINT `order_ibfk_1` FOREIGN KEY (`glassID`) REFERENCES `glass` (`glassID`),
  ADD CONSTRAINT `order_ibfk_2` FOREIGN KEY (`machineID`) REFERENCES `machine` (`machineID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `order_ibfk_3` FOREIGN KEY (`recipeID`) REFERENCES `recipe` (`recipeID`) ON DELETE SET NULL ON UPDATE SET NULL;

--
-- Constraints for table `orderitem`
--
ALTER TABLE `orderitem`
  ADD CONSTRAINT `OrderItem_ibfk_1` FOREIGN KEY (`orderID`) REFERENCES `order` (`orderID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `OrderItem_ibfk_2` FOREIGN KEY (`bottleID`) REFERENCES `bottle` (`bottleID`);

--
-- Constraints for table `recipe`
--
ALTER TABLE `recipe`
  ADD CONSTRAINT `Recipe_ibfk_1` FOREIGN KEY (`glassID`) REFERENCES `glass` (`glassID`),
  ADD CONSTRAINT `Recipe_ibfk_2` FOREIGN KEY (`categoryID`) REFERENCES `category` (`categoryID`);

--
-- Constraints for table `recipeitem`
--
ALTER TABLE `recipeitem`
  ADD CONSTRAINT `RecipeItem_ibfk_1` FOREIGN KEY (`recipeID`) REFERENCES `recipe` (`recipeID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `RecipeItem_ibfk_2` FOREIGN KEY (`categoryID`) REFERENCES `category` (`categoryID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
