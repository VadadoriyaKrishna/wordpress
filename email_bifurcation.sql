-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jul 23, 2024 at 02:03 PM
-- Server version: 8.0.37-0ubuntu0.20.04.3
-- PHP Version: 7.4.3-4ubuntu2.23

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `email_bifurcation`
--

-- --------------------------------------------------------

--
-- Table structure for table `mails`
--

CREATE TABLE `mails` (
  `Id` int NOT NULL,
  `sender_id` varchar(50) DEFAULT NULL,
  `receiver_id` varchar(50) DEFAULT NULL,
  `type` varchar(25) DEFAULT NULL,
  `flag` int DEFAULT NULL,
  `attachment` varchar(100) DEFAULT NULL,
  `mail_time` varchar(100) DEFAULT NULL,
  `storing_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `mails`
--

INSERT INTO `mails` (`Id`, `sender_id`, `receiver_id`, `type`, `flag`, `attachment`, `mail_time`, `storing_time`) VALUES
(1, 'hello@hubspot.com', 'kishuvadadoriya@gmail.com', 'Inquiry', 0, '', 'Wed, 17 Jul 2024 22:19:36 -0400', '2024-07-19 16:49:49'),
(2, 'updates@email.mysivi.ai', 'kishuvadadoriya@gmail.com', 'Inquiry', 0, '', 'Thu, 18 Jul 2024 02:41:39 +0000', '2024-07-19 16:49:50'),
(3, 'Coursera@m.learn.coursera.org', 'kishuvadadoriya@gmail.com', 'Complaint', 0, '', 'Thu, 18 Jul 2024 17:14:52 +0000', '2024-07-19 16:49:52');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `mails`
--
ALTER TABLE `mails`
  ADD PRIMARY KEY (`Id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `mails`
--
ALTER TABLE `mails`
  MODIFY `Id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
