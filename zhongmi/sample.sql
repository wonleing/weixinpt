SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

CREATE TABLE `zhongmi_main` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `title` varchar(50),
    `description` varchar(1000),
    `pic` varchar(200),
    `link` varchar(200),
    `type` integer NOT NULL
)
;
CREATE TABLE `zhongmi_channel` (
    `channelid` integer NOT NULL PRIMARY KEY,
    `name` varchar(50),
    `address` varchar(50),
    `phone` varchar(50),
    `password` varchar(50)
)
;
CREATE TABLE `zhongmi_customer` (
    `customerid` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `wxid` varchar(200),
    `name` varchar(50),
    `phone` varchar(50),
    `gender` varchar(10),
    `age` integer,
    `adress` varchar(200),
    `channelid` integer NOT NULL DEFAULT 5,
    `grade` integer NOT NULL DEFAULT 1,
    `saler` varchar(50),
    `amount` double precision NOT NULL DEFAULT 0,
    `point` double precision NOT NULL DEFAULT 0
)
;
CREATE TABLE `zhongmi_items` (
    `itemid` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(50),
    `price` double precision
)
;
CREATE TABLE `zhongmi_sales` (
    `salesid` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `customerid` integer NOT NULL,
    `channelid` integer,
    `date` datetime NOT NULL,
    `total` double precision NOT NULL DEFAULT 0
)
;
CREATE TABLE `zhongmi_salesdetail` (
    `detailid` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `salesid` integer NOT NULL,
    `itemid` integer NOT NULL,
    `amount` integer NOT NULL DEFAULT 0
)
;
CREATE TABLE `zhongmi_shops` (
    `grade` integer NOT NULL PRIMARY KEY,
    `discount` double precision NOT NULL DEFAULT 1,
    `description` varchar(100),
    `link` varchar(200)
)
;
