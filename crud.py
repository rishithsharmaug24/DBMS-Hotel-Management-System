from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional
from datetime import date
import models, schemas


# ============= HOTEL CRUD =============
def create_hotel(db: Session, hotel: schemas.HotelCreate):
    db_hotel = models.Hotel(**hotel.model_dump())
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

def get_hotel(db: Session, hotel_id: int):
    return db.query(models.Hotel).filter(models.Hotel.hotel_id == hotel_id).first()

def get_hotels(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Hotel).offset(skip).limit(limit).all()

def update_hotel(db: Session, hotel_id: int, hotel: schemas.HotelCreate):
    db_hotel = get_hotel(db, hotel_id)
    if db_hotel:
        for key, value in hotel.model_dump().items():
            setattr(db_hotel, key, value)
        db.commit()
        db.refresh(db_hotel)
    return db_hotel

def delete_hotel(db: Session, hotel_id: int):
    db_hotel = get_hotel(db, hotel_id)
    if db_hotel:
        db.delete(db_hotel)
        db.commit()
        return True
    return False


# ============= EMPLOYEE CRUD =============
def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_emp = models.Employee(**employee.model_dump())
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp

def get_employee(db: Session, emp_id: int):
    return db.query(models.Employee).filter(models.Employee.emp_id == emp_id).first()

def get_employees_by_hotel(db: Session, hotel_id: int):
    return db.query(models.Employee).filter(models.Employee.hotel_id == hotel_id).all()


# ============= ROOM CRUD =============
def create_room(db: Session, room: schemas.RoomCreate):
    db_room = models.Room(**room.model_dump())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def get_room(db: Session, room_id: int):
    return db.query(models.Room).filter(models.Room.room_id == room_id).first()

def get_available_rooms(db: Session, hotel_id: int, check_in: date, check_out: date):
    """Get rooms available for given dates"""
    booked_rooms = db.query(models.Booking.room_id).filter(
        and_(
            models.Booking.status.in_(['Confirmed', 'Checked-In']),
            or_(
                and_(models.Booking.check_in_date <= check_in, models.Booking.check_out_date > check_in),
                and_(models.Booking.check_in_date < check_out, models.Booking.check_out_date >= check_out),
                and_(models.Booking.check_in_date >= check_in, models.Booking.check_out_date <= check_out)
            )
        )
    ).subquery()
    
    return db.query(models.Room).filter(
        and_(
            models.Room.hotel_id == hotel_id,
            models.Room.status == models.RoomStatus.AVAILABLE,
            ~models.Room.room_id.in_(booked_rooms)
        )
    ).all()


# ============= GUEST CRUD =============
def create_guest(db: Session, guest: schemas.GuestCreate):
    db_guest = models.Guest(name=guest.name, email=guest.email)
    db.add(db_guest)
    db.flush()
    
    # Add phone numbers
    for phone_data in guest.phones:
        db_phone = models.GuestPhone(
            guest_id=db_guest.guest_id,
            phone=phone_data.phone,
            phone_type=phone_data.phone_type
        )
        db.add(db_phone)
    
    db.commit()
    db.refresh(db_guest)
    return db_guest

def get_guest(db: Session, guest_id: int):
    return db.query(models.Guest).filter(models.Guest.guest_id == guest_id).first()

def search_guests(db: Session, search_term: str):
    return db.query(models.Guest).filter(
        or_(
            models.Guest.name.like(f"%{search_term}%"),
            models.Guest.email.like(f"%{search_term}%")
        )
    ).all()


# ============= BOOKING CRUD =============
def create_booking(db: Session, booking: schemas.BookingCreate):
    db_booking = models.Booking(**booking.model_dump())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    
    # Recalculate total (triggers will handle this in actual DB)
    recalc_booking_total(db, db_booking.booking_id)
    return db_booking

def get_booking(db: Session, booking_id: int):
    return db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()

def get_bookings_by_guest(db: Session, guest_id: int):
    return db.query(models.Booking).filter(models.Booking.guest_id == guest_id).all()

def recalc_booking_total(db: Session, booking_id: int):
    """Recalculate booking total amount"""
    booking = get_booking(db, booking_id)
    if not booking:
        return
    
    # Calculate room total
    days = (booking.check_out_date - booking.check_in_date).days
    room_total = days * booking.room.price_per_night
    
    # Calculate services total
    services_total = sum(
        su.quantity * su.service.price 
        for su in booking.service_usages
    )
    
    booking.total_amount = room_total + services_total
    db.commit()
    db.refresh(booking)
    return booking


# ============= PAYMENT CRUD =============
def create_payment(db: Session, payment: schemas.PaymentCreate):
    db_payment = models.Payment(**payment.model_dump())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payments_by_booking(db: Session, booking_id: int):
    return db.query(models.Payment).filter(models.Payment.booking_id == booking_id).all()


# ============= SERVICE CRUD =============
def create_service(db: Session, service: schemas.ServiceCreate):
    db_service = models.Service(**service.model_dump())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

def get_service(db: Session, service_id: int):
    return db.query(models.Service).filter(models.Service.service_id == service_id).first()

def get_services(db: Session):
    return db.query(models.Service).all()


# ============= SERVICE USAGE CRUD =============
def add_service_to_booking(db: Session, service_usage: schemas.ServiceUsageCreate):
    db_usage = models.ServiceUsage(**service_usage.model_dump())
    db.add(db_usage)
    db.commit()
    db.refresh(db_usage)
    
    # Recalculate booking total
    recalc_booking_total(db, service_usage.booking_id)
    return db_usage