-- phpMyAdmin SQL Dump
-- version 5.1.3-2.el7.remi
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Mar 07, 2022 at 11:48 PM
-- Server version: 10.6.5-MariaDB-log
-- PHP Version: 7.4.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cs340_chankaih`
--

-- --------------------------------------------------------

--
-- Table structure for table `Authors`
--

DROP TABLE IF EXISTS `Authors`;
CREATE TABLE `Authors` (
  `author_id` int(11) NOT NULL,
  `author_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Authors`
--

INSERT INTO `Authors` (`author_id`, `author_name`) VALUES
(7, 'Geoffrey Chaucer'),
(4, 'Homer'),
(1, 'J. K. Rowling'),
(6, 'Jane Austen'),
(2, 'John Steinbeck'),
(5, 'Lewis Carroll'),
(3, 'William Shakespeare');

-- --------------------------------------------------------

--
-- Table structure for table `Books`
--

DROP TABLE IF EXISTS `Books`;
CREATE TABLE `Books` (
  `book_id` int(11) NOT NULL,
  `author_id` int(11) NOT NULL,
  `publisher_id` int(11) DEFAULT NULL,
  `title` varchar(255) NOT NULL,
  `year` int(11) DEFAULT NULL,
  `cost` decimal(10,2) DEFAULT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Books`
--

INSERT INTO `Books` (`book_id`, `author_id`, `publisher_id`, `title`, `year`, `cost`, `quantity`) VALUES
(1, 1, 1, 'Harry Potter and the Sorcerer\'s Stone', 1999, '8.99', 100),
(2, 1, 1, 'Harry Potter and the Chamber of Secrets', 2000, '9.99', 100),
(3, 1, 1, 'Harry Potter and the Prisoner of Azkaban', 2001, '9.99', 100),
(4, 1, 1, 'Harry Potter and the Goblet of Fire', 2002, '12.99', 99),
(5, 1, 1, 'Harry Potter and the Order of the Phoenix', 2004, '12.99', 99),
(6, 1, 1, 'Harry Potter and the Half-Blood Prince', 2006, '12.99', 99),
(7, 1, 1, 'Harry Potter and the Deathly Hallows', 2009, '14.99', 100),
(8, 2, 2, 'Of Mice and Men', 1993, '10.99', 100),
(9, 3, 3, 'Macbeth (Folger Shakespeare Library Series)', 2003, '6.99', 99),
(10, 3, 3, 'Much Ado about Nothing (Folger Shakespeare Library Series)', 2004, '6.99', 99),
(11, 3, 3, 'Romeo and Juliet (Folger Shakespeare Library Series)', 2004, '6.99', 100),
(12, 4, 2, 'The Odyssey: (Penguin Classics Deluxe Edition)', 1997, '16.99', 99),
(13, 5, 4, 'Alice\'s Adventures in Wonderland', 2008, '6.99', 99),
(14, 6, 2, 'Pride and Prejudice', 2002, '8.99', 100),
(15, 7, 2, 'The Canterbury Tales', 2003, '10.99', 99);

-- --------------------------------------------------------

--
-- Table structure for table `Customers`
--

DROP TABLE IF EXISTS `Customers`;
CREATE TABLE `Customers` (
  `customer_id` int(11) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `street` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `zip` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Customers`
--

INSERT INTO `Customers` (`customer_id`, `first_name`, `last_name`, `email`, `phone`, `street`, `city`, `zip`) VALUES
(1, 'Bob', 'Smith', 'bobsmith1@gmail.com', '510-927-2998', '23 Main Street', 'San Francisco', 94016),
(2, 'Katie', 'Johnson', 'katj24@gmail.com', '510-821-5272', '624 1st Street', 'San Jose', 95050),
(3, 'Liam', 'Garcia', 'gliam@gmail.com', '408-863-6151', '9465 E street', 'Oakland', 94501),
(4, 'Jen', 'Jones', 'jjones55@gmail.com', '207-851-9875', '565 West Avenue', 'Portland', 97086),
(5, 'Oliver', 'Holden', 'oliverh95@gmail.com', '207-821-9152', '64 Second Street', 'Portland', 97207),
(6, 'June', 'Miller', 'Jmill2@gmail.com', '541-821-3675', '256 University Ave', 'Corvallis', 97330),
(7, 'Alex', 'Brown', 'albrown54@gmail.com', '510-218-3780', '35 7th Street', 'Oakland', 94604),
(8, 'Emma', 'Davis', 'emdav94@gmail.com', '415-863-8210', '350 3rd Street', 'San Francisco', 94107);

-- --------------------------------------------------------

--
-- Table structure for table `Orders`
--

DROP TABLE IF EXISTS `Orders`;
CREATE TABLE `Orders` (
  `order_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `total_cost` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Orders`
--

INSERT INTO `Orders` (`order_id`, `customer_id`, `date`, `total_cost`) VALUES
(1, 8, '2022-02-08', '15.38'),
(2, 3, '2022-02-18', '41.87'),
(3, 2, '2022-02-11', '7.69'),
(4, 7, '2022-02-14', '29.08');

-- --------------------------------------------------------

--
-- Table structure for table `Order_details`
--

DROP TABLE IF EXISTS `Order_details`;
CREATE TABLE `Order_details` (
  `order_details_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `cost` decimal(10,2) NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Order_details`
--

INSERT INTO `Order_details` (`order_details_id`, `order_id`, `book_id`, `cost`, `quantity`) VALUES
(1, 1, 9, '6.99', 1),
(2, 1, 10, '6.99', 1),
(3, 2, 4, '12.99', 1),
(4, 2, 5, '12.99', 1),
(5, 2, 6, '12.99', 1),
(6, 3, 13, '6.99', 1),
(7, 4, 12, '16.99', 1),
(8, 4, 15, '10.99', 1);

-- --------------------------------------------------------

--
-- Table structure for table `Publishers`
--

DROP TABLE IF EXISTS `Publishers`;
CREATE TABLE `Publishers` (
  `publisher_id` int(11) NOT NULL,
  `publisher_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Publishers`
--

INSERT INTO `Publishers` (`publisher_id`, `publisher_name`) VALUES
(2, 'Penguin Publishing Group'),
(4, 'Penguin Young Readers Group'),
(1, 'Scholastic, Inc.'),
(3, 'Simon & Schuster');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Authors`
--
ALTER TABLE `Authors`
  ADD PRIMARY KEY (`author_id`),
  ADD UNIQUE KEY `author_name` (`author_name`);

--
-- Indexes for table `Books`
--
ALTER TABLE `Books`
  ADD PRIMARY KEY (`book_id`),
  ADD UNIQUE KEY `author_id_2` (`author_id`,`publisher_id`,`title`),
  ADD KEY `author_id` (`author_id`),
  ADD KEY `publisher_id` (`publisher_id`);

--
-- Indexes for table `Customers`
--
ALTER TABLE `Customers`
  ADD PRIMARY KEY (`customer_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `Orders`
--
ALTER TABLE `Orders`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `customer_id` (`customer_id`);

--
-- Indexes for table `Order_details`
--
ALTER TABLE `Order_details`
  ADD PRIMARY KEY (`order_details_id`),
  ADD UNIQUE KEY `order_id_2` (`order_id`,`book_id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `book_id` (`book_id`);

--
-- Indexes for table `Publishers`
--
ALTER TABLE `Publishers`
  ADD PRIMARY KEY (`publisher_id`),
  ADD UNIQUE KEY `publisher_name` (`publisher_name`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Authors`
--
ALTER TABLE `Authors`
  MODIFY `author_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `Books`
--
ALTER TABLE `Books`
  MODIFY `book_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `Customers`
--
ALTER TABLE `Customers`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `Orders`
--
ALTER TABLE `Orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `Order_details`
--
ALTER TABLE `Order_details`
  MODIFY `order_details_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `Publishers`
--
ALTER TABLE `Publishers`
  MODIFY `publisher_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Books`
--
ALTER TABLE `Books`
  ADD CONSTRAINT `Books_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `Authors` (`author_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `Books_ibfk_2` FOREIGN KEY (`publisher_id`) REFERENCES `Publishers` (`publisher_id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `Orders`
--
ALTER TABLE `Orders`
  ADD CONSTRAINT `Orders_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `Customers` (`customer_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Order_details`
--
ALTER TABLE `Order_details`
  ADD CONSTRAINT `Order_details_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `Orders` (`order_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `Order_details_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `Books` (`book_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
