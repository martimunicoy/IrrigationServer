DROP DATABASE IF EXISTS irrigation_db;
CREATE DATABASE irrigation_db;
CREATE USER IF NOT EXISTS 'irrigation_program'@'localhost';
GRANT ALL ON irrigation_db.* TO 'irrigation_program'@'localhost';
SET PASSWORD FOR 'irrigation_program'@'localhost' = PASSWORD('1234');
FLUSH PRIVILEGES;
USE irrigation_db;
CREATE TABLE slots ( id TINYINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
description VARCHAR(100),
active BOOLEAN
);
CREATE TABLE schedule (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
time TIME NOT NULL
);
CREATE TABLE status (id TINYINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
label VARCHAR(20) NOT NULL, status BOOLEAN, value TINYINT
);
INSERT INTO status (label, status) VALUES ('running', FALSE);
INSERT INTO status (label, value) VALUES ('position', NULL);
