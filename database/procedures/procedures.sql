USE hotel_management_system;

DELIMITER $$

DROP PROCEDURE IF EXISTS hotel_management_system.recalc_booking_total$$

CREATE PROCEDURE hotel_management_system.recalc_booking_total(IN p_booking_id INT)
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
END$$

DELIMITER ;