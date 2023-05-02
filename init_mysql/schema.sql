CREATE DATABASE company;
USE company;

CREATE USER 'api'@'%' IDENTIFIED BY 'api_pass';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, REFERENCES ON company.workers TO 'api'@'%';

CREATE USER 'website'@'%' IDENTIFIED BY 'website_pass';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, REFERENCES ON company.workers TO 'website'@'%';
FLUSH PRIVILEGES;

CREATE TABLE workers(
    id int AUTO_INCREMENT,
    name varchar(20),
    team varchar(20),
    tasks_received int,
    tasks_in_progress int,
    tasks_finished int,
    PRIMARY KEY (id)
);

INSERT INTO workers( name, team, tasks_received, tasks_in_progress, tasks_finished ) 
VALUES 
    ("frank", "lemon", 20, 5, 15),
    ("john", "lemon", 15, 5, 10),
    ("bill", "lemon", 35, 10, 25),

    ("dave", "orange", 45, 20, 25),
    ("jorge", "orange", 10, 0, 10),
    
    ("dan", "banana", 30, 15, 15),
    ("seth", "banana", 20, 0, 20),
    ("wade", "banana", 15, 3, 12),
    ("riley", "banana", 15, 0, 15)
    ;