USE hotel_management_system;

DELETE FROM service_usage;
DELETE FROM payment;
DELETE FROM booking;
DELETE FROM guest_phone;
DELETE FROM service;
DELETE FROM employee;
DELETE FROM room;
DELETE FROM guest;
DELETE FROM hotel;

INSERT INTO hotel (name, city, address) VALUES
('Grand Plaza Hotel', 'Delhi', 'Connaught Place, New Delhi'),
('Taj Luxury Resort', 'Mumbai', 'Marine Drive, Mumbai'),
('Palace Hotel', 'Agra', 'Near Taj Mahal, Agra');

INSERT INTO employee (hotel_id, name, role, salary, hired_date) VALUES
(1, 'Rajesh Kumar', 'Manager', 50000.00, '2023-01-15'),
(1, 'Priya Singh', 'Receptionist', 25000.00, '2023-06-01'),
(1, 'Amit Patel', 'Housekeeping', 18000.00, '2023-03-20'),
(2, 'Neha Sharma', 'Manager', 52000.00, '2023-02-01'),
(2, 'Vikram Desai', 'Receptionist', 26000.00, '2023-07-10');

INSERT INTO room (hotel_id, room_number, room_type, price_per_night, status) VALUES
(1, '101', 'Single', 2000.00, 'Available'),
(1, '102', 'Double', 3500.00, 'Available'),
(1, '103', 'Suite', 5000.00, 'Booked'),
(1, '104', 'Deluxe', 4500.00, 'Available'),
(2, '201', 'Single', 2200.00, 'Available'),
(2, '202', 'Double', 3800.00, 'Available'),
(3, '301', 'Suite', 5500.00, 'Available');

INSERT INTO guest (name, email) VALUES
('John Smith', 'john.smith@example.com'),
('Sarah Johnson', 'sarah.johnson@example.com'),
('Michael Brown', 'michael.brown@example.com'),
('Emma Williams', 'emma.williams@example.com'),
('David Lee', 'david.lee@example.com');

INSERT INTO guest_phone (guest_id, phone, phone_type) VALUES
(1, '9876543210', 'Mobile'),
(2, '9123456789', 'Mobile'),
(3, '8765432109', 'Mobile'),
(4, '9999888777', 'Mobile'),
(5, '8888777666', 'Home');

INSERT INTO service (service_name, price) VALUES
('Room Service', 500.00),
('Laundry Service', 200.00),
('Spa Service', 1500.00),
('Breakfast Buffet', 800.00),
('Airport Transfer', 1000.00),
('WiFi Package', 100.00);

INSERT INTO booking (guest_id, room_id, check_in_date, check_out_date, booking_date, status) VALUES
(1, 1, '2025-11-10', '2025-11-12', '2025-11-04', 'Confirmed'),
(2, 2, '2025-11-15', '2025-11-17', '2025-11-04', 'Confirmed'),
(3, 3, '2025-12-01', '2025-12-05', '2025-11-04', 'Confirmed');

INSERT INTO payment (booking_id, payment_date, amount, payment_method, payment_status) VALUES
(1, '2025-11-04', 4000.00, 'Card', 'Paid'),
(2, '2025-11-04', 7000.00, 'UPI', 'Paid'),
(3, '2025-11-04', 10000.00, 'Cash', 'Paid');

INSERT INTO service_usage (booking_id, service_id, quantity) VALUES
(1, 1, 2),
(1, 2, 1),
(2, 3, 1),
(2, 4, 2),
(3, 5, 1);