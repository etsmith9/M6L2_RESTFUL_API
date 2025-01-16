CREATE DATABASE FITNESS_CENTER_MANAGER;

USE FITNESS_CENTER_MANAGER;
CREATE TABLE Members (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT
);
CREATE TABLE WorkoutSessions (
    session_id INT PRIMARY KEY,
    member_id INT,
    session_date DATE,
    session_time VARCHAR(50),
    activity VARCHAR(255),
    FOREIGN KEY (member_id) REFERENCES Members(id)
);

INSERT INTO Members (id, name, age)
VALUES ('001', 'Emily Smith', '30'),
    ('002', 'Harry Dhillon', '40'),
	('003', 'Amrit Singh', '17'),
	('004', 'Indie Dhillon', '20');
    
INSERT INTO WorkoutSessions (Session_id, member_id, session_date, session_time, activity)
VALUES ('8001', '001', '2024-12-12', '0900', 'yoga'),
	('8002', '002', '2024-12-12', '0910', 'pickleball'),
    ('8003', '003', '2024-12-13', '1010', 'swimming'),
    ('8004', '004', '2024-12-13', '0900', 'yoga');
    
UPDATE WorkoutSessions
SET session_time = 1800
WHERE member_id = 001;

DELETE FROM WorkoutSessions
WHERE member_id = 004;

DELETE FROM Members
WHERE id = 004;
    
SELECT * from Members
SELECT * from WorkoutSessions