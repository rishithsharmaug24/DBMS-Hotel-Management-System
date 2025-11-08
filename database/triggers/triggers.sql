USE hotel_management_system;

DROP TRIGGER IF EXISTS trg_booking_after_insert;
DROP TRIGGER IF EXISTS trg_booking_after_update;
DROP TRIGGER IF EXISTS trg_su_after_insert;
DROP TRIGGER IF EXISTS trg_su_after_update;
DROP TRIGGER IF EXISTS trg_su_after_delete;
DROP TRIGGER IF EXISTS trg_room_after_update;
DROP TRIGGER IF EXISTS trg_service_after_update;

-- Trigger 1
CREATE TRIGGER trg_room_status_update
AFTER UPDATE ON booking
FOR EACH ROW
BEGIN
    UPDATE room 
    SET status = CASE 
        WHEN NEW.status = 'Checked-In' THEN 'Booked'
        WHEN NEW.status = 'Checked-Out' THEN 'Available'
        ELSE status
    END
    WHERE room_id = NEW.room_id;
END;

-- Trigger 2
CREATE TRIGGER trg_booking_status_checkin
BEFORE UPDATE ON booking
FOR EACH ROW
BEGIN
    IF NEW.status = 'Checked-In' AND OLD.status = 'Confirmed' THEN
        IF CURDATE() < NEW.check_in_date THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Cannot check in before check-in date';
        END IF;
    END IF;
END;

-- Trigger 3
CREATE TRIGGER trg_booking_status_checkout
BEFORE UPDATE ON booking
FOR EACH ROW
BEGIN
    IF NEW.status = 'Checked-Out' AND OLD.status = 'Checked-In' THEN
        IF CURDATE() < NEW.check_out_date THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Cannot check out before check-out date';
        END IF;
    END IF;
END;

-- Trigger 4
CREATE TRIGGER trg_validate_dates_before_insert
BEFORE INSERT ON booking
FOR EACH ROW
BEGIN
    IF NEW.check_out_date <= NEW.check_in_date THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Check-out date must be after check-in date';
    END IF;

    IF NEW.check_in_date < CURDATE() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Check-in date cannot be in the past';
    END IF;
END;

-- Trigger 5
CREATE TRIGGER trg_validate_dates_before_update
BEFORE UPDATE ON booking
FOR EACH ROW
BEGIN
    IF NEW.check_out_date <= NEW.check_in_date THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Check-out date must be after check-in date';
    END IF;
END;
