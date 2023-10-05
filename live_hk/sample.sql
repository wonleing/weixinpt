CREATE TABLE `live_hk_record` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(20) NOT NULL,
    `phone` varchar(20) NOT NULL,
    `type` varchar(20) NOT NULL,
    `date` datetime NOT NULL
)
;
CREATE TABLE `live_hk_main` (
    `id` integer NOT NULL PRIMARY KEY,
    `title` varchar(50) NOT NULL,
    `description` varchar(1000) NOT NULL,
    `pic` varchar(200) NOT NULL,
    `link` varchar(200) NOT NULL,
    `type` integer NOT NULL
)
;
CREATE TABLE `live_hk_topic` (
    `id` integer NOT NULL PRIMARY KEY,
    `description` varchar(1000) NOT NULL,
    `score` integer NOT NULL
)
;
CREATE TABLE `live_hk_member` (
    `wxid` varchar(50) NOT NULL PRIMARY KEY,
    `name` varchar(20) NOT NULL,
    `phone` varchar(20) NOT NULL,
    `point` integer NOT NULL
)
;
