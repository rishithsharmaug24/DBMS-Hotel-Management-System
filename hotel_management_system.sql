-- ============================================================================
-- HOTEL MANAGEMENT SYSTEM - SAMPLE DATABASE
-- Complete SQL script to create database with sample data
-- ============================================================================

-- Create database
DROP DATABASE IF EXISTS hotel_management;
CREATE DATABASE hotel_management;
USE hotel_management;

-- ============================================================================
-- TABLE CREATION
-- ============================================================================

-- 1. Hotel Table
CREATE TABLE hotel (
    hotel_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    address VARCHAR(200) NOT NULL,
    INDEX idx_city (city)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Employee Table
CREATE TABLE employee (
    emp_id VARCHAR(50) PRIMARY KEY,
    hotel_id VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL,
    salary DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (hotel_id) REFERENCES hotel(hotel_id) ON DELETE CASCADE,
    INDEX idx_hotel (hotel_id),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Guest Table
CREATE TABLE guest (
    guest_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Room Table
CREATE TABLE room (
    room_id VARCHAR(50) PRIMARY KEY,
    hotel_id VARCHAR(50) NOT NULL,
    room_type VARCHAR(50) NOT NULL,
    price_per_night DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'available',
    FOREIGN KEY (hotel_id) REFERENCES hotel(hotel_id) ON DELETE CASCADE,
    INDEX idx_hotel (hotel_id),
    INDEX idx_status (status),
    INDEX idx_type (room_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Booking Table
CREATE TABLE booking (
    booking_id VARCHAR(50) PRIMARY KEY,
    guest_id VARCHAR(50) NOT NULL,
    room_id VARCHAR(50) NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (guest_id) REFERENCES guest(guest_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES room(room_id) ON DELETE CASCADE,
    INDEX idx_guest (guest_id),
    INDEX idx_room (room_id),
    INDEX idx_dates (check_in_date, check_out_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. Payment Table
CREATE TABLE payment (
    payment_id VARCHAR(50) PRIMARY KEY,
    booking_id VARCHAR(50) NOT NULL,
    payment_date DATE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    method VARCHAR(50) NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES booking(booking_id) ON DELETE CASCADE,
    INDEX idx_booking (booking_id),
    INDEX idx_date (payment_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. Service Table
CREATE TABLE service (
    service_id VARCHAR(50) PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    INDEX idx_name (service_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. Service Usage Table (Junction Table)
CREATE TABLE service_usage (
    booking_id VARCHAR(50) NOT NULL,
    service_id VARCHAR(50) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    total_price DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (booking_id, service_id),
    FOREIGN KEY (booking_id) REFERENCES booking(booking_id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES service(service_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- SAMPLE DATA INSERTION
-- ============================================================================

-- Insert Hotels
INSERT INTO hotel (hotel_id, name, city, address) VALUES
('HTL001', 'Grand Plaza Hotel', 'Mumbai', '123 Marine Drive, Mumbai 400001'),
('HTL002', 'Royal Palace Hotel', 'Delhi', '456 Connaught Place, Delhi 110001'),
('HTL003', 'Beach Resort & Spa', 'Goa', '789 Calangute Beach, Goa 403516'),
('HTL004', 'Mountain View Hotel', 'Shimla', '321 Mall Road, Shimla 171001'),
('HTL005', 'Lake Palace Hotel', 'Udaipur', '654 Lake Pichola, Udaipur 313001');

-- Insert Employees
INSERT INTO employee (emp_id, hotel_id, name, role, salary) VALUES
-- Grand Plaza Hotel (Mumbai)
('EMP001', 'HTL001', 'Rajesh Kumar', 'General Manager', 80000.00),
('EMP002', 'HTL001', 'Priya Sharma', 'Front Desk Manager', 45000.00),
('EMP003', 'HTL001', 'Amit Patel', 'Housekeeping Supervisor', 35000.00),
('EMP004', 'HTL001', 'Sneha Gupta', 'Receptionist', 28000.00),
('EMP005', 'HTL001', 'Vikram Singh', 'Chef', 50000.00),

-- Royal Palace Hotel (Delhi)
('EMP006', 'HTL002', 'Sunita Verma', 'General Manager', 85000.00),
('EMP007', 'HTL002', 'Arjun Malhotra', 'Front Desk Manager', 48000.00),
('EMP008', 'HTL002', 'Neha Kapoor', 'Receptionist', 30000.00),
('EMP009', 'HTL002', 'Ravi Kumar', 'Bellboy', 22000.00),

-- Beach Resort (Goa)
('EMP010', 'HTL003', 'Kavita Desai', 'General Manager', 75000.00),
('EMP011', 'HTL003', 'Rahul Mehta', 'Activities Coordinator', 38000.00),
('EMP012', 'HTL003', 'Anjali Nair', 'Spa Manager', 45000.00),

-- Mountain View (Shimla)
('EMP013', 'HTL004', 'Suresh Reddy', 'General Manager', 70000.00),
('EMP014', 'HTL004', 'Pooja Iyer', 'Receptionist', 26000.00),

-- Lake Palace (Udaipur)
('EMP015', 'HTL005', 'Manish Jain', 'General Manager', 90000.00),
('EMP016', 'HTL005', 'Deepika Shah', 'Concierge', 42000.00);

-- Insert Guests
INSERT INTO guest (guest_id, name, phone, email) VALUES
('GST001', 'Arjun Mehta', '+91-9876543210', 'arjun.mehta@email.com'),
('GST002', 'Sneha Desai', '+91-9876543211', 'sneha.desai@email.com'),
('GST003', 'Rahul Kapoor', '+91-9876543212', 'rahul.kapoor@email.com'),
('GST004', 'Neha Gupta', '+91-9876543213', 'neha.gupta@email.com'),
('GST005', 'Vikram Sharma', '+91-9876543214', 'vikram.sharma@email.com'),
('GST006', 'Priya Singh', '+91-9876543215', 'priya.singh@email.com'),
('GST007', 'Amit Kumar', '+91-9876543216', 'amit.kumar@email.com'),
('GST008', 'Kavita Patel', '+91-9876543217', 'kavita.patel@email.com'),
('GST009', 'Ravi Verma', '+91-9876543218', 'ravi.verma@email.com'),
('GST010', 'Anjali Reddy', '+91-9876543219', 'anjali.reddy@email.com');

-- Insert Rooms
INSERT INTO room (room_id, hotel_id, room_type, price_per_night, status) VALUES
-- Grand Plaza Hotel (Mumbai)
('RM001', 'HTL001', 'Deluxe', 5000.00, 'occupied'),
('RM002', 'HTL001', 'Suite', 10000.00, 'occupied'),
('RM003', 'HTL001', 'Standard', 3000.00, 'available'),
('RM004', 'HTL001', 'Deluxe', 5000.00, 'available'),
('RM005', 'HTL001', 'Presidential Suite', 20000.00, 'available'),

-- Royal Palace Hotel (Delhi)
('RM006', 'HTL002', 'Presidential Suite', 25000.00, 'available'),
('RM007', 'HTL002', 'Deluxe', 8000.00, 'available'),
('RM008', 'HTL002', 'Suite', 12000.00, 'occupied'),
('RM009', 'HTL002', 'Standard', 4000.00, 'available'),

-- Beach Resort (Goa)
('RM010', 'HTL003', 'Beach Villa', 15000.00, 'occupied'),
('RM011', 'HTL003', 'Deluxe Sea View', 8000.00, 'available'),
('RM012', 'HTL003', 'Standard', 4000.00, 'available'),
('RM013', 'HTL003', 'Premium Villa', 18000.00, 'available'),

-- Mountain View (Shimla)
('RM014', 'HTL004', 'Mountain View Suite', 7000.00, 'available'),
('RM015', 'HTL004', 'Deluxe', 5000.00, 'available'),
('RM016', 'HTL004', 'Standard', 3500.00, 'occupied'),

-- Lake Palace (Udaipur)
('RM017', 'HTL005', 'Royal Suite', 22000.00, 'available'),
('RM018', 'HTL005', 'Lake View Deluxe', 12000.00, 'available'),
('RM019', 'HTL005', 'Palace Room', 9000.00, 'available'),
('RM020', 'HTL005', 'Standard', 5000.00, 'available');

-- Insert Services
INSERT INTO service (service_id, service_name, price) VALUES
('SRV001', 'Room Service', 500.00),
('SRV002', 'Laundry Service', 300.00),
('SRV003', 'Spa & Massage', 2000.00),
('SRV004', 'Airport Pickup', 1500.00),
('SRV005', 'Mini Bar', 800.00),
('SRV006', 'Breakfast Buffet', 600.00),
('SRV007', 'Gym Access', 400.00),
('SRV008', 'Swimming Pool Access', 300.00),
('SRV009', 'Business Center', 500.00),
('SRV010', 'City Tour', 2500.00);

-- Insert Bookings
INSERT INTO booking (booking_id, guest_id, room_id, check_in_date, check_out_date, total_amount) VALUES
-- Current bookings (occupied rooms)
('BKG001', 'GST001', 'RM001', '2025-11-01', '2025-11-04', 15000.00),
('BKG002', 'GST002', 'RM002', '2025-11-01', '2025-11-03', 20000.00),
('BKG003', 'GST003', 'RM010', '2025-10-30', '2025-11-05', 75000.00),
('BKG004', 'GST004', 'RM008', '2025-10-31', '2025-11-03', 36000.00),
('BKG005', 'GST005', 'RM016', '2025-11-01', '2025-11-02', 3500.00),

-- Past bookings
('BKG006', 'GST006', 'RM003', '2025-10-15', '2025-10-18', 9000.00),
('BKG007', 'GST007', 'RM007', '2025-10-20', '2025-10-23', 24000.00),
('BKG008', 'GST008', 'RM011', '2025-10-10', '2025-10-15', 40000.00),

-- Future bookings
('BKG009', 'GST009', 'RM006', '2025-11-10', '2025-11-13', 75000.00),
('BKG010', 'GST010', 'RM017', '2025-11-15', '2025-11-18', 66000.00);

-- Insert Payments
INSERT INTO payment (payment_id, booking_id, payment_date, amount, method) VALUES
-- Payments for BKG001
('PAY001', 'BKG001', '2025-11-01', 10000.00, 'Credit Card'),
('PAY002', 'BKG001', '2025-11-02', 5000.00, 'UPI'),

-- Payments for BKG002
('PAY003', 'BKG002', '2025-11-01', 20000.00, 'Debit Card'),

-- Payments for BKG003
('PAY004', 'BKG003', '2025-10-30', 50000.00, 'Cash'),
('PAY005', 'BKG003', '2025-11-02', 25000.00, 'Credit Card'),

-- Payments for BKG004
('PAY006', 'BKG004', '2025-10-31', 36000.00, 'UPI'),

-- Payments for BKG005
('PAY007', 'BKG005', '2025-11-01', 3500.00, 'Cash'),

-- Payments for past bookings
('PAY008', 'BKG006', '2025-10-15', 9000.00, 'Credit Card'),
('PAY009', 'BKG007', '2025-10-20', 24000.00, 'Debit Card'),
('PAY010', 'BKG008', '2025-10-10', 40000.00, 'Bank Transfer'),

-- Advance payment for future booking
('PAY011', 'BKG009', '2025-11-01', 20000.00, 'Credit Card'),
('PAY012', 'BKG010', '2025-11-02', 30000.00, 'UPI');

-- Insert Service Usage
INSERT INTO service_usage (booking_id, service_id, quantity, total_price) VALUES
-- BKG001 services
('BKG001', 'SRV001', 2, 1000.00),  -- Room Service x2
('BKG001', 'SRV003', 1, 2000.00),  -- Spa
('BKG001', 'SRV006', 3, 1800.00),  -- Breakfast x3

-- BKG002 services
('BKG002', 'SRV004', 1, 1500.00),  -- Airport Pickup
('BKG002', 'SRV005', 2, 1600.00),  -- Mini Bar x2

-- BKG003 services
('BKG003', 'SRV001', 5, 2500.00),  -- Room Service x5
('BKG003', 'SRV003', 2, 4000.00),  -- Spa x2
('BKG003', 'SRV010', 1, 2500.00),  -- City Tour

-- BKG004 services
('BKG004', 'SRV002', 2, 600.00),   -- Laundry x2
('BKG004', 'SRV006', 3, 1800.00),  -- Breakfast x3

-- BKG006 services (past booking)
('BKG006', 'SRV001', 1, 500.00),
('BKG006', 'SRV006', 3, 1800.00);

-- ============================================================================
-- USEFUL VIEWS FOR REPORTING
-- ============================================================================

-- View: Booking Details with Guest and Room Info
CREATE OR REPLACE VIEW vw_booking_details AS
SELECT 
    b.booking_id,
    b.check_in_date,
    b.check_out_date,
    b.total_amount,
    g.guest_id,
    g.name AS guest_name,
    g.email AS guest_email,
    g.phone AS guest_phone,
    r.room_id,
    r.room_type,
    r.price_per_night,
    r.status AS room_status,
    h.hotel_id,
    h.name AS hotel_name,
    h.city AS hotel_city,
    DATEDIFF(b.check_out_date, b.check_in_date) AS nights_stayed
FROM booking b
JOIN guest g ON b.guest_id = g.guest_id
JOIN room r ON b.room_id = r.room_id
JOIN hotel h ON r.hotel_id = h.hotel_id;

-- View: Payment Summary by Booking
CREATE OR REPLACE VIEW vw_payment_summary AS
SELECT 
    b.booking_id,
    b.total_amount,
    COALESCE(SUM(p.amount), 0) AS total_paid,
    b.total_amount - COALESCE(SUM(p.amount), 0) AS balance,
    CASE 
        WHEN b.total_amount - COALESCE(SUM(p.amount), 0) = 0 THEN 'Paid'
        WHEN b.total_amount - COALESCE(SUM(p.amount), 0) > 0 THEN 'Pending'
        ELSE 'Overpaid'
    END AS payment_status
FROM booking b
LEFT JOIN payment p ON b.booking_id = p.booking_id
GROUP BY b.booking_id, b.total_amount;

-- View: Hotel Occupancy Status
CREATE OR REPLACE VIEW vw_hotel_occupancy AS
SELECT 
    h.hotel_id,
    h.name AS hotel_name,
    h.city,
    COUNT(r.room_id) AS total_rooms,
    SUM(CASE WHEN r.status = 'available' THEN 1 ELSE 0 END) AS available_rooms,
    SUM(CASE WHEN r.status = 'occupied' THEN 1 ELSE 0 END) AS occupied_rooms,
    SUM(CASE WHEN r.status = 'maintenance' THEN 1 ELSE 0 END) AS maintenance_rooms,
    ROUND((SUM(CASE WHEN r.status = 'occupied' THEN 1 ELSE 0 END) / COUNT(r.room_id)) * 100, 2) AS occupancy_rate
FROM hotel h
LEFT JOIN room r ON h.hotel_id = r.hotel_id
GROUP BY h.hotel_id, h.name, h.city;

-- View: Service Revenue
CREATE OR REPLACE VIEW vw_service_revenue AS
SELECT 
    s.service_id,
    s.service_name,
    s.price AS unit_price,
    COALESCE(SUM(su.quantity), 0) AS total_quantity_sold,
    COALESCE(SUM(su.total_price), 0) AS total_revenue
FROM service s
LEFT JOIN service_usage su ON s.service_id = su.service_id
GROUP BY s.service_id, s.service_name, s.price;

-- ============================================================================
-- USEFUL QUERIES FOR TESTING
-- ============================================================================

-- Check all tables have data
SELECT 'Hotels' AS table_name, COUNT(*) AS record_count FROM hotel
UNION ALL
SELECT 'Employees', COUNT(*) FROM employee
UNION ALL
SELECT 'Guests', COUNT(*) FROM guest
UNION ALL
SELECT 'Rooms', COUNT(*) FROM room
UNION ALL
SELECT 'Bookings', COUNT(*) FROM booking
UNION ALL
SELECT 'Payments', COUNT(*) FROM payment
UNION ALL
SELECT 'Services', COUNT(*) FROM service
UNION ALL
SELECT 'Service Usage', COUNT(*) FROM service_usage;

-- ============================================================================
-- COMPLETION MESSAGE
-- ============================================================================

SELECT '✓ Database created successfully!' AS Status;
SELECT '✓ 5 Hotels with 20 rooms' AS Data;
SELECT '✓ 16 Employees across all hotels' AS Data;
SELECT '✓ 10 Registered guests' AS Data;
SELECT '✓ 10 Bookings (5 current, 3 past, 2 future)' AS Data;
SELECT '✓ 12 Payments recorded' AS Data;
SELECT '✓ 10 Services available' AS Data;
SELECT '✓ Multiple service usages recorded' AS Data;
SELECT '✓ 4 Reporting views created' AS Data;
SELECT 'Database is ready for testing!' AS Message;