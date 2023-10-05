SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

CREATE TABLE `yukangyuan_product` (
    `productid` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(50) NOT NULL,
    `pic` varchar(200) NOT NULL,
    `type` varchar(20) NOT NULL,
    `brand` varchar(20) NOT NULL,
    `detail` varchar(200) NOT NULL,
    `storage` integer NOT NULL,
    `flag` varchar(20) NOT NULL,
    `price1` integer NOT NULL,
    `price2` integer NOT NULL,
    `price3` integer NOT NULL
)
;
CREATE TABLE `yukangyuan_saler` (
    `salerid` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(20) NOT NULL,
    `password` varchar(50) NOT NULL,
    `description` varchar(50) NOT NULL,
    `a_total` integer NOT NULL,
    `a_order` integer NOT NULL
)
;
CREATE TABLE `yukangyuan_customer` (
    `customerid` varchar(20) NOT NULL PRIMARY KEY,
    `password` varchar(50) NOT NULL,
    `name` varchar(50) NOT NULL,
    `contact` varchar(10) NOT NULL,
    `phone` varchar(20) NOT NULL,
    `address` varchar(200) NOT NULL,
    `salerid` integer NOT NULL,
    `a_amount` integer NOT NULL,
    `privilege` varchar(20) NOT NULL
)
;
CREATE TABLE `yukangyuan_order` (
    `orderid` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `customerid` varchar(20) NOT NULL,
    `date` datetime NOT NULL,
    `total` integer NOT NULL,
    `status` integer NOT NULL
)
;
CREATE TABLE `yukangyuan_orderdetail` (
    `detailid` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `orderid` integer NOT NULL,
    `productid` integer NOT NULL,
    `amount` integer NOT NULL,
    `total` integer NOT NULL,
    `status` integer NOT NULL
)
;
CREATE TABLE `yukangyuan_support` (
    `supportid` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `customerid` varchar(20) NOT NULL,
    `reason` varchar(50) NOT NULL,
    `detail` varchar(200) NOT NULL,
    `total` integer NOT NULL,
    `date` datetime NOT NULL
)
;
CREATE TABLE `yukangyuan_report` (
    `reportid` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `salerid` integer NOT NULL,
    `content` varchar(500) NOT NULL,
    `date` datetime NOT NULL
)
;
CREATE TABLE `yukangyuan_return` (
    `returnid` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `customerid` varchar(20) NOT NULL,
    `detail` varchar(500) NOT NULL,
    `total` integer NOT NULL,
    `date` datetime NOT NULL
)
;
