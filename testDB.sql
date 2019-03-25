/********************************************************************************
    Using the Chinook DB as an example /
/*******************************************************************************
   Drop database if it exists
********************************************************************************/
DROP DATABASE IF EXISTS `vehicleList`;


/*******************************************************************************
   Create database
********************************************************************************/
CREATE DATABASE `vehicleList`;


USE `vehicleList`;


/*******************************************************************************
   Create Tables
********************************************************************************/
CREATE TABLE `Region`
(
    `region_id` INT NOT NULL AUTO_INCREMENT,
    `region_name` VARCHAR(40) NOT NULL,
    PRIMARY KEY  (`region_id`)
);

CREATE TABLE `Make`
(
    `make_id` INT NOT NULL AUTO_INCREMENT,
    `make_name` VARCHAR(30) NOT NULL,
    PRIMARY KEY  (`make_id`)
);

CREATE TABLE `Model`
(
    `model_id` INT NOT NULL AUTO_INCREMENT,
    `model_name` VARCHAR(160) NOT NULL,
    PRIMARY KEY  (`model_id`),
    FOREIGN KEY ('make_id') REFERENCES Make('make_id')
);

CREATE TABLE `Model_Year`
(
    `model_year_id` INT NOT NULL AUTO_INCREMENT,
    `year_num` INT NOT NULL,
    PRIMARY KEY  (`model_year_id`),
    FOREIGN KEY ('model_id') REFERENCES Model('model_id')
);

CREATE TABLE `Trans`
(
    `trans_id` INT NOT NULL AUTO_INCREMENT,
    `trans_desc` VARCHAR(20) NOT NULL,
    PRIMARY KEY  (`trans_id`)
);

CREATE TABLE `Popularity`
(
    `popularity_id` INT NOT NULL AUTO_INCREMENT,
    `popularity_num` INT NOT NULL,
    PRIMARY KEY  (`popularity_id`)
);

CREATE TABLE `Stats`
(
    `stats_id` INT NOT NULL AUTO_INCREMENT,
    `hp_amount` INT NOT NULL,
    `torque_amount` INT NOT NULL,
    `accel_time` INT NOT NULL,
    PRIMARY KEY  (`stats_id`)
);

CREATE TABLE `drive`
(
    `drive_id` INT NOT NULL AUTO_INCREMENT,
    `drive_desc` VARCHAR(20) NOT NULL,
    PRIMARY KEY  (`drive_id`)
);

CREATE TABLE `Chassy_Type`
(
    `chassy_id` INT NOT NULL AUTO_INCREMENT,
    `chassy_desc` VARCHAR(30) NOT NULL,
    PRIMARY KEY  (`chassy_id`)
);

CREATE TABLE `Users`
(
    `user_id` INT NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(30) NOT NULL,
    `password` VARCHAR(30) NOT NULL,
    PRIMARY KEY (`user_id`)
)

CREATE TABLE `Car`
(
    `car_id` INT NOT NULL AUTO_INCREMENT,
    FOREIGN KEY ('make_id') REFERENCES Make('make_id'),
    FOREIGN KEY ('model_id') REFERENCES Model('model_id'),
    `img_url` VARCHAR(250),
    FOREIGN KEY ('model_year_id') REFERENCES Model_Year('model_year_id'),
    FOREIGN KEY ('region_id') REFERENCES Region('region_id'),
    FOREIGN KEY ('stats_id') REFERENCES Stats('stats_id'),
    FOREIGN KEY ('trans_id') REFERENCES Trans('trans_id'),
    FOREIGN KEY ('chassy_id') REFERENCES Chassy('chassy_id'),
    FOREIGN KEY ('drive_id') REFERENCES Drive('drive_id'),
    FOREIGN KEY ('popularity_id') REFERENCES Popularity('popularity_id'),
    FOREIGN KEY ('user_id') REFERENCES Users('user_id'),
    PRIMARY KEY (`car_id`)
);