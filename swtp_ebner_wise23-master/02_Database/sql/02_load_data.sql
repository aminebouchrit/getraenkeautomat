SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;

SET time_zone = "+00:00";
USE `drink_machine`;

INSERT INTO `user` (`userID`, `name`, `password`) VALUES
(1, 'admin', 'superSecret');

COMMIT;
START TRANSACTION;

INSERT INTO `category` (`categoryID`, `parent_categoryID`, `name`) VALUES
(1, NULL, 'Getränke'),
(2, 1, 'Säfte'),
(3, 2, 'Fruchtsäfte'),
(4, 2, 'Kokosnuss-Wasser'),
(5, 2, 'Saftschorle'),
(6, 3, 'Multivitaminsaft'),
(8, 5, 'Apfelschorle'),
(9, 1, 'Cocktails'),
(10, 1, 'Softdrinks'),
(11, 10, 'Fanta'),
(12, 10, 'Spezi'),
(13, 10, 'Cola'),
(14, 13, 'Coca-Cola'),
(15, 1, 'Longdrinks'),
(16, 1, 'Bier'),
(17, 16, 'Weizenbier'),
(18, 1, 'Spirituose'),
(19, 18, 'Wein'),
(20, 18, 'Vodka'),
(21, 18, 'Whiskey'),
(22, 18, 'Rum'),
(23, 19, 'Weisswein'),
(24, 19, 'Rotwein'),
(25, 20, 'Absolut Vodka'),
(26, 21, 'Jack Daniels'),
(27, 22, 'White'),
(28, 22, 'Black'),
(29, 1, 'Wasser'),
(30, 29, 'Stilles Wasser'),
(31, 29, 'Wasser mit Kohlensäure'),
(32, 13, 'Vita Cola'),
(33, 13, 'Pepsi Cola'),
(34, 31, 'Förstina Premium Spritzig'),
(35, 31, 'Frankenbrunnen Spritzig'),
(36, 30, 'Gerolsteiner Naturell Gourmet'),
(37, 30, 'Frankenbrunnen Still'),
(38, 17, 'Krombacher Weizen'),
(39, 1, 'Biermischgetränk'),
(40, 3, 'Sauerkirschnektar'),
(41, 3, 'Bananennektar'),
(42, 2, 'Zitrussäfte'),
(7, 42, 'Orangensaft'),
(43, 42, 'Zitronensaft');

COMMIT;
START TRANSACTION;

INSERT INTO `bottle` (`bottleID`, `categoryID`, `name`, `density`, `max_capacity`, `alcohol_percentage`, `price`, `pic_url`) VALUES
(1, 14, 'Coca-Cola', 1.03, 1000, 0, 1.75, 'https://cdn02.plentymarkets.com/q7p0kwea05gv/item/images/4285/full/35570c.jpg'),
(2, 32, 'Vita Cola', 1.03, 1000, 0, 1.50, 'https://cdn02.plentymarkets.com/q7p0kwea05gv/item/images/2568/full/37901c.jpg'),
(3, 11, 'Fanta', 1.03, 1000, 0, 1.75, 'https://cdn02.plentymarkets.com/q7p0kwea05gv/item/images/4287/full/35572c.jpg'),
(4, 36, 'Gerolsteiner Naturell Gourmet', 1.00, 750, 0, 3.50, 'https://cdn02.plentymarkets.com/q7p0kwea05gv/item/images/4232/full/35336b.jpg'),
(5, 37, 'Frankenbrunnen Still', 1.00, 1000, 0, 1.55, 'https://cdn02.plentymarkets.com/q7p0kwea05gv/item/images/4141/full/205750.jpg'),
(6, 34, 'Förstina Premium Spritzig', 1.00, 1000, 0, 1.08, 'https://cdn02.plentymarkets.com/q7p0kwea05gv/item/images/4107/full/31400c.jpg'),
(7, 35, 'Frankenbrunnen Spritzig', 1.00, 1000, 0, 1.17, 'https://cdn02.plentymarkets.com/q7p0kwea05gv/item/images/4140/full/201419.jpg'),
(8, 38, 'Krombacher Weizen', 1.00, 500, 5, 2.70, 'https://cdn02.plentymarkets.com/q7p0kwea05gv/item/images/7991/full/20132c.jpg'),
(9, 40, 'Sachsenobst Sauerkirsche', 1.00, 1000, 0, 3.0, 'https://cdn02.plentymarkets.com/q7p0kwea05gv/item/images/4603/full/38305a.jpg'),
(10, 41, 'Sachsenobst Banane', 1.00, 1000, 0, 2.83, 'https://cdn02.plentymarkets.com/q7p0kwea05gv/item/images/4618/full/38327a.jpg'),
(11, 43, 'Zitronensaft', 1.00, 1000, 0, 5.90, 'https://cdn02.plentymarkets.com/q7p0kwea05gv/item/images/4204/full/35261c.jpg');

COMMIT;
START TRANSACTION;

INSERT INTO `machine` (`machineID`, `name`) VALUES
(1, 'DrinkMachine'),
(2, 'Future Machine');

INSERT INTO `bottleitem` (`bottleItemID`, `machineID`, `bottleID`, `position_cm`, `pump_pin`, `led_pin`, `current_capacity`) VALUES
(1, 2, 1, 31, 4, 33, 300),
(2, 2, 3, 60, 8, 36, 300),
(3, 2, 8, 91, 10, 34, 300);

INSERT INTO `bottleitem` (`bottleItemID`, `machineID`, `bottleID`, `position_cm`, `pump_pin`, `led_pin`, `current_capacity`) VALUES
(4, 1, 9, 31, 4, 33, 300),
(5, 1, 10, 60, 8, 36, 300),
(6, 1, 11, 91, 10, 34, 300);

COMMIT;
START TRANSACTION;

INSERT INTO `glass`(`glassID`, `amount_ml`, `weight_g`) VALUES
(1, '500', '236'),
(2, '100', '194');

COMMIT;
START TRANSACTION;

INSERT INTO `recipe` (`recipeID`, `glassID`, `categoryID`, `name`, `price`, `pic_url`) VALUES
(1, 1, 11, 'Fanta', 2.00, "https://cdn02.plentymarkets.com/q7p0kwea05gv/item/images/4287/full/35572c.jpg"),
(2, 1, 14, 'Coca-Cola', 2.50, "https://cdn02.plentymarkets.com/q7p0kwea05gv/item/images/4285/full/35570c.jpg"),
(3, 1, 12, 'Spezi', 2.99, 'https://cdn02.plentymarkets.com/q7p0kwea05gv/item/images/3739/full/20953c.jpg'),
(4, 1, 32, 'Vita Cola', 2.00, "https://cdn02.plentymarkets.com/q7p0kwea05gv/item/images/2568/full/37901c.jpg"),
(5, 1, 38, 'Krombacher Weizen', 3.10, "https://cdn02.plentymarkets.com/q7p0kwea05gv/item/images/7991/full/20132c.jpg"),
(6, 1, 39, 'Colaweizen', 3.00, "https://cdn02.plentymarkets.com/q7p0kwea05gv/item/images/7991/full/20132c.jpg");

INSERT INTO `recipe`(`recipeID`, `glassID`, `categoryID`, `name`, `price`, `rating_value`, `rating_number`, `pic_url`) VALUES
(7, 2, 40, 'Sauerkirschnektar', 3.00, 4.00, 1, "https://cdn02.plentymarkets.com/q7p0kwea05gv/item/images/4603/full/38305a.jpg"),
(8, 2, 41, 'Bananennektar', 3.00, 4.50, 2, "https://cdn02.plentymarkets.com/q7p0kwea05gv/item/images/4618/full/38327a.jpg"),
(9, 2, 3, 'KiBa', 3.10, 4.33, 3, "https://cdn02.plentymarkets.com/q7p0kwea05gv/item/images/4618/full/38327a.jpg");

COMMIT;
START TRANSACTION;

INSERT INTO `recipeitem` (`recipeItemID`, `recipeID`, `categoryID`, `amount_ml`) VALUES
(1, 1, 11, 15),
(2, 2, 14, 20),
(3, 3, 11, 10),
(4, 3, 13, 10),
(5, 4, 32, 15),
(6, 5, 38, 12),
(7, 6, 17, 10),
(8, 6, 13, 10),
(9, 7, 40, 30),
(10, 8, 41, 30),
(11, 9, 40, 15),
(12, 9, 41, 15);

COMMIT;