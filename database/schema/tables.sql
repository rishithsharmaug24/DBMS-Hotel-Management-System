USE hotel_management_system;

DROP TABLE IF EXISTS service_usage;
DROP TABLE IF EXISTS payment;
DROP TABLE IF EXISTS booking;
DROP TABLE IF EXISTS guest_phone;
DROP TABLE IF EXISTS service;
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS room;
DROP TABLE IF EXISTS guest;
DROP TABLE IF EXISTS hotel;

CREATE TABLE hotel (
    hotel_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    city VARCHAR(100) NOT NULL,
    address VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (hotel_id),
    UNIQUE KEY uq_hotel_name (name),
    INDEX idx_hotel_city (city)
) ENGINE=InnoDB;

CREATE TABLE employee (
    emp_id INT NOT NULL AUTO_INCREMENT,
    hotel_id INT NOT NULL,
    name VARCHAR(150) NOT NULL,
    role VARCHAR(100),
    salary DECIMAL(12,2),
    hired_date DATE DEFAULT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (emp_id),
    CONSTRAINT fk_employee_hotel FOREIGN KEY (hotel_id)
        REFERENCES hotel(hotel_id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_employee_hotel (hotel_id),
    INDEX idx_employee_role (role)
) ENGINE=InnoDB;

CREATE TABLE room (
    room_id INT NOT NULL AUTO_INCREMENT,
    hotel_id INT NOT NULL,
    room_number VARCHAR(20) NOT NULL,
    room_type VARCHAR(50) NOT NULL,
    price_per_night DECIMAL(10,2) NOT NULL,
    status ENUM('Available','Booked','Maintenance') NOT NULL DEFAULT 'Available',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (room_id),
    UNIQUE KEY uq_room_unique (hotel_id, room_number),
    CONSTRAINT fk_room_hotel FOREIGN KEY (hotel_id)
        REFERENCES hotel(hotel_id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_room_hotel (hotel_id),
    INDEX idx_room_type (room_type)
) ENGINE=InnoDB;

CREATE TABLE guest (
    guest_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (guest_id),
    UNIQUE KEY uq_guest_email (email),
    INDEX idx_guest_name (name)
) ENGINE=InnoDB;

CREATE TABLE guest_phone (
    guest_id INT NOT NULL,
    phone VARCHAR(30) NOT NULL,
    phone_type ENUM('Mobile','Home','Work','Other') DEFAULT 'Mobile',
    PRIMARY KEY (guest_id, phone),
    CONSTRAINT fk_gp_guest FOREIGN KEY (guest_id)
        REFERENCES guest(guest_id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_guest_phone (phone)
) ENGINE=InnoDB;

CREATE TABLE service (
    service_id INT NOT NULL AUTO_INCREMENT,
    service_name VARCHAR(150) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (service_id),
    UNIQUE KEY uq_service_name (service_name),
    INDEX idx_service_price (price)
) ENGINE=InnoDB;

CREATE TABLE booking (
    booking_id INT NOT NULL AUTO_INCREMENT,
    guest_id INT NOT NULL,
    room_id INT NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    booking_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    status ENUM('Confirmed','Checked-In','Checked-Out','Cancelled') NOT NULL DEFAULT 'Confirmed',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (booking_id),
    CONSTRAINT fk_booking_guest FOREIGN KEY (guest_id)
        REFERENCES guest(guest_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_booking_room FOREIGN KEY (room_id)
        REFERENCES room(room_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CHECK (check_out_date > check_in_date),
    INDEX idx_booking_guest (guest_id),
    INDEX idx_booking_room (room_id),
    INDEX idx_booking_dates (check_in_date, check_out_date)
) ENGINE=InnoDB;

CREATE TABLE payment (
    payment_id INT NOT NULL AUTO_INCREMENT,
    booking_id INT NOT NULL,
    payment_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    amount DECIMAL(12,2) NOT NULL,
    payment_method ENUM('Cash','Card','UPI') NOT NULL,
    payment_status ENUM('Paid','Pending','Failed') NOT NULL DEFAULT 'Paid',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (payment_id),
    CONSTRAINT fk_payment_booking FOREIGN KEY (booking_id)
        REFERENCES booking(booking_id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_payment_booking (booking_id),
    INDEX idx_payment_status (payment_status)
) ENGINE=InnoDB;

CREATE TABLE service_usage (
    booking_id INT NOT NULL,
    service_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (booking_id, service_id),
    CONSTRAINT fk_su_booking FOREIGN KEY (booking_id)
        REFERENCES booking(booking_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_su_service FOREIGN KEY (service_id)
        REFERENCES service(service_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_su_service (service_id)
) ENGINE=InnoDB;