USE hotel_management_system;

-- Ensure proper indexing for performance
CREATE INDEX idx_booking_status ON booking(status);
CREATE INDEX idx_payment_method ON payment(payment_method);
CREATE INDEX idx_room_status ON room(status);
CREATE INDEX idx_guest_email ON guest(email);
CREATE INDEX idx_service_name ON service(service_name);
