BEGIN;
CREATE TABLE `dfth_source` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `sourcename` varchar(50) NOT NULL,
    `number` integer NOT NULL,
    `type` varchar(20) NOT NULL
)
;
CREATE TABLE `dfth_product` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `productname` varchar(50) NOT NULL,
    `number` integer NOT NULL,
    `type` varchar(20) NOT NULL
)
;
CREATE TABLE `dfth_supplyer` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `supplyername` varchar(20) NOT NULL,
    `address` varchar(50) NOT NULL,
    `phone` varchar(50) NOT NULL
)
;
CREATE TABLE `dfth_customer` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `customername` varchar(50) NOT NULL,
    `type` varchar(20) NOT NULL,
    `district` varchar(20) NOT NULL,
    `location` varchar(20) NOT NULL,
    `contact` varchar(10) NOT NULL,
    `phone` varchar(20) NOT NULL,
    `address` varchar(200) NOT NULL,
    `invoiceinfo` varchar(200) NOT NULL
)
;
CREATE TABLE `dfth_employee` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `employeename` varchar(50) NOT NULL,
    `position` varchar(20) NOT NULL,
    `phone` varchar(20) NOT NULL,
    `password` varchar(50) NOT NULL,
    `auth` varchar(20) NOT NULL
)
;
CREATE TABLE `dfth_contract` (
    `contractid` varchar(50) NOT NULL PRIMARY KEY,
    `customername` integer NOT NULL,
    `summary` varchar(200) NOT NULL,
    `total` integer NOT NULL,
    `date` datetime NOT NULL
)
;
ALTER TABLE `dfth_contract` ADD CONSTRAINT `customername_refs_id_b788aa21` FOREIGN KEY (`customername`) REFERENCES `dfth_customer` (`id`);
CREATE TABLE `dfth_purchase` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `supplyername` integer NOT NULL,
    `sourcename` integer NOT NULL,
    `number` integer NOT NULL,
    `price` integer NOT NULL,
    `date` datetime NOT NULL,
    `keepdate` varchar(50) NOT NULL,
    `location` varchar(50) NOT NULL
)
;
ALTER TABLE `dfth_purchase` ADD CONSTRAINT `sourcename_refs_id_fb11afe5` FOREIGN KEY (`sourcename`) REFERENCES `dfth_source` (`id`);
ALTER TABLE `dfth_purchase` ADD CONSTRAINT `supplyername_refs_id_f1759d89` FOREIGN KEY (`supplyername`) REFERENCES `dfth_supplyer` (`id`);
CREATE TABLE `dfth_consume` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `employeename` integer NOT NULL,
    `sourcename` integer NOT NULL,
    `number` integer NOT NULL,
    `date` datetime NOT NULL
)
;
ALTER TABLE `dfth_consume` ADD CONSTRAINT `sourcename_refs_id_bbcfc8a1` FOREIGN KEY (`sourcename`) REFERENCES `dfth_source` (`id`);
ALTER TABLE `dfth_consume` ADD CONSTRAINT `employeename_refs_id_4074977d` FOREIGN KEY (`employeename`) REFERENCES `dfth_employee` (`id`);
CREATE TABLE `dfth_produce` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `productname` integer NOT NULL,
    `number` integer NOT NULL,
    `date` datetime NOT NULL,
    `keepdate` varchar(50) NOT NULL
)
;
ALTER TABLE `dfth_produce` ADD CONSTRAINT `productname_refs_id_03f44e76` FOREIGN KEY (`productname`) REFERENCES `dfth_product` (`id`);
CREATE TABLE `dfth_sale` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `productname` integer NOT NULL,
    `customername` integer NOT NULL,
    `contractid` varchar(50) NOT NULL,
    `number` integer NOT NULL,
    `date` datetime NOT NULL,
    `keepdate` varchar(50) NOT NULL,
    `price` integer NOT NULL,
    `invoice` varchar(50) NOT NULL
)
;
ALTER TABLE `dfth_sale` ADD CONSTRAINT `productname_refs_id_e6dcc333` FOREIGN KEY (`productname`) REFERENCES `dfth_product` (`id`);
ALTER TABLE `dfth_sale` ADD CONSTRAINT `contractid_refs_contractid_39d205fe` FOREIGN KEY (`contractid`) REFERENCES `dfth_contract` (`contractid`);
ALTER TABLE `dfth_sale` ADD CONSTRAINT `customername_refs_id_b396a2fc` FOREIGN KEY (`customername`) REFERENCES `dfth_customer` (`id`);
CREATE TABLE `dfth_income` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `customername` integer NOT NULL,
    `contractid` varchar(50) NOT NULL,
    `number` integer NOT NULL,
    `date` datetime NOT NULL
)
;
ALTER TABLE `dfth_income` ADD CONSTRAINT `contractid_refs_contractid_2d558d97` FOREIGN KEY (`contractid`) REFERENCES `dfth_contract` (`contractid`);
ALTER TABLE `dfth_income` ADD CONSTRAINT `customername_refs_id_b7c8292a` FOREIGN KEY (`customername`) REFERENCES `dfth_customer` (`id`);
CREATE TABLE `dfth_expense` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `employeename` integer NOT NULL,
    `type` varchar(50) NOT NULL,
    `reason` varchar(50) NOT NULL,
    `number` integer NOT NULL,
    `date` datetime NOT NULL,
    `status` varchar(50) NOT NULL
)
;
ALTER TABLE `dfth_expense` ADD CONSTRAINT `employeename_refs_id_050ee969` FOREIGN KEY (`employeename`) REFERENCES `dfth_employee` (`id`);
CREATE TABLE `dfth_notice` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `text` varchar(500) NOT NULL,
    `date` datetime NOT NULL,
    `status` integer NOT NULL
)
;
CREATE TABLE `dfth_device` (
    `deviceid` varchar(50) NOT NULL PRIMARY KEY,
    `devicename` varchar(50) NOT NULL,
    `buydate` varchar(50) NOT NULL,
    `price` integer NOT NULL
)
;

COMMIT;
