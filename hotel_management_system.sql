-- =========================================
-- RESET DATABASE
-- =========================================
DROP DATABASE IF EXISTS hotel_management_system;
CREATE DATABASE hotel_management_system;
USE hotel_management_system;

-- =========================================
-- HOTEL
-- =========================================
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

-- =========================================
-- EMPLOYEE
-- =========================================
DROP TABLE IF EXISTS employee;
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

-- =========================================
-- ROOM
-- =========================================
DROP TABLE IF EXISTS room;
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

-- =========================================
-- GUEST
-- =========================================
DROP TABLE IF EXISTS guest;
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

-- =========================================
-- GUEST_PHONE
-- =========================================
DROP TABLE IF EXISTS guest_phone;
CREATE TABLE guest_phone (
  guest_id INT NOT NULL,
  phone VARCHAR(30) NOT NULL,
  phone_type ENUM('Mobile','Home','Work','Other') DEFAULT 'Mobile',
  PRIMARY KEY (guest_id, phone),
  CONSTRAINT fk_gp_guest FOREIGN KEY (guest_id)
    REFERENCES guest(guest_id) ON DELETE CASCADE ON UPDATE CASCADE,
  INDEX idx_guest_phone (phone)
) ENGINE=InnoDB;

-- =========================================
-- BOOKING
-- =========================================
DROP TABLE IF EXISTS booking;
CREATE TABLE booking (
  booking_id INT NOT NULL AUTO_INCREMENT,
  guest_id INT NOT NULL,
  room_id INT NOT NULL,
  check_in_date DATE NOT NULL,
  check_out_date DATE NOT NULL,
  booking_date DATE NOT NULL DEFAULT (CURRENT_DATE),
  status ENUM('Confirmed','Checked-In','Checked-Out','Cancelled') NOT NULL DEFAULT 'Confirmed',
  total_amount DECIMAL(12,2) NOT NULL DEFAULT 0.00,
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

-- =========================================
-- PAYMENT
-- =========================================
DROP TABLE IF EXISTS payment;
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

-- =========================================
-- SERVICE
-- =========================================
DROP TABLE IF EXISTS service;
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

-- =========================================
-- SERVICE_USAGE
-- =========================================
DROP TABLE IF EXISTS service_usage;
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

-- =========================================
-- VIEWS
-- =========================================
DROP VIEW IF EXISTS booking_service_line;
CREATE VIEW booking_service_line AS
SELECT su.booking_id,
       su.service_id,
       s.service_name,
       su.quantity,
       s.price AS unit_price,
       (su.quantity * s.price) AS line_total
FROM service_usage su
JOIN service s ON su.service_id = s.service_id;

DROP VIEW IF EXISTS booking_totals;
CREATE VIEW booking_totals AS
SELECT b.booking_id,
       b.guest_id,
       b.room_id,
       b.check_in_date,
       b.check_out_date,
       (GREATEST(DATEDIFF(b.check_out_date, b.check_in_date), 0) * r.price_per_night) AS room_total,
       COALESCE(SUM(s.price * su.quantity), 0) AS services_total,
       (GREATEST(DATEDIFF(b.check_out_date, b.check_in_date), 0) * r.price_per_night)
         + COALESCE(SUM(s.price * su.quantity), 0) AS booking_total
FROM booking b
JOIN room r ON b.room_id = r.room_id
LEFT JOIN service_usage su ON b.booking_id = su.booking_id
LEFT JOIN service s ON su.service_id = s.service_id
GROUP BY b.booking_id, b.guest_id, b.room_id, b.check_in_date, b.check_out_date, r.price_per_night;

-- =========================================
-- PROCEDURE + TRIGGERS
-- =========================================
DELIMITER $$

-- Procedure to recalc total amount
DROP PROCEDURE IF EXISTS recalc_booking_total $$
CREATE PROCEDURE recalc_booking_total(IN p_booking_id INT)
BEGIN
  DECLARE v_room_total DECIMAL(12,2) DEFAULT 0;
  DECLARE v_services_total DECIMAL(12,2) DEFAULT 0;
  DECLARE v_total DECIMAL(12,2) DEFAULT 0;

  SELECT GREATEST(DATEDIFF(b.check_out_date, b.check_in_date), 0) * r.price_per_night
  INTO v_room_total
  FROM booking b
  JOIN room r ON b.room_id = r.room_id
  WHERE b.booking_id = p_booking_id;

  SELECT COALESCE(SUM(s.price * su.quantity), 0)
  INTO v_services_total
  FROM service_usage su
  JOIN service s ON su.service_id = s.service_id
  WHERE su.booking_id = p_booking_id;

  SET v_total = COALESCE(v_room_total, 0) + COALESCE(v_services_total, 0);

  UPDATE booking
  SET total_amount = v_total, updated_at = CURRENT_TIMESTAMP
  WHERE booking_id = p_booking_id;
END $$

-- Booking triggers
DROP TRIGGER IF EXISTS trg_booking_after_insert $$
CREATE TRIGGER trg_booking_after_insert
AFTER INSERT ON booking
FOR EACH ROW
BEGIN
  CALL recalc_booking_total(NEW.booking_id);
END $$

DROP TRIGGER IF EXISTS trg_booking_after_update $$
CREATE TRIGGER trg_booking_after_update
AFTER UPDATE ON booking
FOR EACH ROW
BEGIN
  IF (OLD.room_id <> NEW.room_id)
     OR (OLD.check_in_date <> NEW.check_in_date)
     OR (OLD.check_out_date <> NEW.check_out_date) THEN
    CALL recalc_booking_total(NEW.booking_id);
  END IF;
END $$

-- Service usage triggers
DROP TRIGGER IF EXISTS trg_su_after_insert $$
CREATE TRIGGER trg_su_after_insert
AFTER INSERT ON service_usage
FOR EACH ROW
BEGIN
  CALL recalc_booking_total(NEW.booking_id);
END $$

DROP TRIGGER IF EXISTS trg_su_after_update $$
CREATE TRIGGER trg_su_after_update
AFTER UPDATE ON service_usage
FOR EACH ROW
BEGIN
  IF (OLD.quantity <> NEW.quantity) OR (OLD.service_id <> NEW.service_id) THEN
    CALL recalc_booking_total(NEW.booking_id);
  END IF;
END $$

DROP TRIGGER IF EXISTS trg_su_after_delete $$
CREATE TRIGGER trg_su_after_delete
AFTER DELETE ON service_usage
FOR EACH ROW
BEGIN
  CALL recalc_booking_total(OLD.booking_id);
END $$

-- Room trigger
DROP TRIGGER IF EXISTS trg_room_after_update $$
CREATE TRIGGER trg_room_after_update
AFTER UPDATE ON room
FOR EACH ROW
BEGIN
  DECLARE done INT DEFAULT 0;
  DECLARE b_id INT;
  DECLARE cur1 CURSOR FOR
    SELECT booking_id FROM booking WHERE room_id = NEW.room_id;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

  IF OLD.price_per_night <> NEW.price_per_night THEN
    OPEN cur1;
    read_loop: LOOP
      FETCH cur1 INTO b_id;
      IF done = 1 THEN
        LEAVE read_loop;
      END IF;
      CALL recalc_booking_total(b_id);
    END LOOP;
    CLOSE cur1;
  END IF;
END $$

-- ✅ Fixed Service trigger (final version)
DROP TRIGGER IF EXISTS trg_service_after_update $$
CREATE TRIGGER trg_service_after_update
AFTER UPDATE ON service
FOR EACH ROW
BEGIN
  DECLARE done2 INT DEFAULT 0;
  DECLARE b2 INT;
  DECLARE cur2 CURSOR FOR
    SELECT DISTINCT booking_id FROM service_usage WHERE service_id = NEW.service_id;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done2 = 1;

  IF OLD.price <> NEW.price THEN
    OPEN cur2;
    read_loop2: LOOP
      FETCH cur2 INTO b2;
      IF done2 = 1 THEN
        LEAVE read_loop2;
      END IF;
      CALL recalc_booking_total(b2);
    END LOOP;
    CLOSE cur2;
  END IF;
END $$

DELIMITER ;



