USE hotel_management_system;

-- ✅ Temporarily disable safe updates & FK checks
SET SQL_SAFE_UPDATES = 0;
SET FOREIGN_KEY_CHECKS = 0;

-- ✅ Safe deletion in correct order
DELETE FROM service_usage;
DELETE FROM payment;
DELETE FROM booking;
DELETE FROM guest_phone;
DELETE FROM service;
DELETE FROM employee;
DELETE FROM room;
DELETE FROM guest;
DELETE FROM hotel;

-- ✅ Re-enable safety and FK checks
SET FOREIGN_KEY_CHECKS = 1;
SET SQL_SAFE_UPDATES = 1;

-- Re-enable constraints and safe mode
SET FOREIGN_KEY_CHECKS = 1;
SET SQL_SAFE_UPDATES = 1;

-- ✅ Now reinsert hotel data
INSERT INTO hotel (hotel_id, name, city, address) VALUES
(1, 'Grand Plaza Hotel', 'Delhi', 'Connaught Place, New Delhi'),
(2, 'Taj Luxury Resort', 'Mumbai', 'Marine Drive, Mumbai'),
(3, 'Palace Hotel', 'Agra', 'Near Taj Mahal, Agra');


-- ------------------------------------------------------------
-- Step 5: Insert Employees
-- ------------------------------------------------------------
INSERT INTO employee (hotel_id, name, role, salary, hired_date) VALUES
(1, 'Rajesh Kumar', 'Manager', 50000.00, '2023-01-15'),
(1, 'Priya Singh', 'Receptionist', 25000.00, '2023-06-01'),
(3, 'Amit Patel', 'Housekeeping', 18000.00, '2023-03-20'),
(2, 'Neha Sharma', 'Manager', 52000.00, '2023-02-01'),
(2, 'Vikram Desai', 'Receptionist', 26000.00, '2023-07-10');
-- ------------------------------------------------------------
-- Step 6: Insert Rooms
-- ------------------------------------------------------------
INSERT INTO room (room_id, hotel_id, room_number, room_type, price_per_night, status)
VALUES
(1, 1, '101', 'Deluxe', 150.00, 'Available'),
(2, 1, '102', 'Standard', 100.00, 'Available'),
(3, 2, '103', 'Suite', 200.00, 'Available'),
(4, 3,  '104', 'Presidential', 'Available');

-- ------------------------------------------------------------
-- Step 7: Insert Guests
-- ------------------------------------------------------------
INSERT INTO guest (name, email) VALUES
('John Smith', 'john.smith@example.com'),
('Sarah Johnson', 'sarah.johnson@example.com'),
('Michael Brown', 'michael.brown@example.com'),
('Emma Williams', 'emma.williams@example.com'),
('David Lee', 'david.lee@example.com');

-- ------------------------------------------------------------
-- Step 8: Insert Guest Phones
-- ------------------------------------------------------------
INSERT INTO guest_phone (guest_id, phone, phone_type) VALUES
(1, '9876543210', 'Mobile'),
(2, '9123456789', 'Mobile'),
(3, '8765432109', 'Mobile'),
(4, '9999888777', 'Mobile'),
(5, '8888777666', 'Home');

-- ------------------------------------------------------------
-- Step 9: Insert Services
-- ------------------------------------------------------------
INSERT INTO service (service_name, price) VALUES
('Room Service', 500.00),
('Laundry Service', 200.00),
('Spa Service', 1500.00),
('Breakfast Buffet', 800.00),
('Airport Transfer', 1000.00),
('WiFi Package', 100.00);

-- ------------------------------------------------------------
-- Step 10: Insert Bookings
-- ------------------------------------------------------------
INSERT INTO booking (guest_id, room_id, check_in_date, check_out_date, booking_date, status) VALUES
(1, 1, '2025-11-10', '2025-11-12', '2025-11-04', 'Confirmed'),
(2, 2, '2025-11-11', '2025-11-17', '2025-11-04', 'Confirmed'),
(3, 3, '2025-11-10', '2025-12-05', '2025-11-04', 'Confirmed'),
(4, 4, '2025-11-12', '2025-12-06', '2025-11-10', 'Confirmed');

-- ------------------------------------------------------------
-- Step 11: Insert Payments
-- ------------------------------------------------------------
INSERT INTO payment (booking_id, payment_date, amount, payment_method, payment_status) VALUES
(1, '2025-11-04', 4000.00, 'Card', 'Paid'),
(2, '2025-11-04', 7000.00, 'UPI', 'Paid'),
(3, '2025-11-04', 10000.00, 'Cash', 'Paid');

-- ------------------------------------------------------------
-- Step 12: Insert Service Usage
-- ------------------------------------------------------------
INSERT INTO service_usage (booking_id, service_id, quantity) VALUES
(1, 1, 2),
(1, 2, 1),
(2, 3, 1),
(2, 4, 2),
(3, 5, 1);

-- ------------------------------------------------------------
-- Step 13: Final Verification Query (optional)
-- ------------------------------------------------------------
-- SELECT * FROM hotel;
-- SELECT * FROM employee;
-- SELECT * FROM room;
-- SELECT * FROM guest;
-- SELECT * FROM booking;
-- SELECT * FROM payment;
-- SELECT * FROM service_usage;
