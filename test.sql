DROP DATABASE IF EXISTS hotel_management_system;

CREATE DATABASE hotel_management_system;

USE hotel_management_system;

DROP TABLE IF EXISTS rooms;

CREATE TABLE rooms (
    room_id INT PRIMARY KEY AUTO_INCREMENT,
    room_number VARCHAR(10),
    room_type VARCHAR(20),
    price DECIMAL(10,2)
);

INSERT INTO rooms (room_number, room_type, price)
VALUES ('101', 'Deluxe', 2500.00);

SELECT * FROM rooms;

