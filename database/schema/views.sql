USE hotel_management_system;

DROP VIEW IF EXISTS booking_service_line;
DROP VIEW IF EXISTS booking_totals;

CREATE VIEW booking_service_line AS
SELECT 
    su.booking_id,
    su.service_id,
    s.service_name,
    su.quantity,
    s.price AS unit_price,
    (su.quantity * s.price) AS line_total
FROM service_usage su
JOIN service s ON su.service_id = s.service_id;

CREATE VIEW booking_totals AS
SELECT 
    b.booking_id,
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