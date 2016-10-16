CREATE DATABASE IF NOT EXISTS todolist;

CREATE USER 'todolistuser' IDENTIFIED BY 'todolistpass';

GRANT ALL ON todolist.* TO 'todolistuser';

USE todolist;

DROP TABLE IF EXISTS todolist;

CREATE TABLE todolist (
id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
end_date DATETIME, 
task VARCHAR(200) NOT NULL );

