from sqlalchemy import (
    Column, Integer, String, DECIMAL, Date, DateTime, 
    Enum, ForeignKey, CheckConstraint, Index, TIMESTAMP
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

# Enums
class RoomStatus(str, enum.Enum):
    AVAILABLE = "Available"
    BOOKED = "Booked"
    MAINTENANCE = "Maintenance"

class BookingStatus(str, enum.Enum):
    CONFIRMED = "Confirmed"
    CHECKED_IN = "Checked-In"
    CHECKED_OUT = "Checked-Out"
    CANCELLED = "Cancelled"

class PaymentMethod(str, enum.Enum):
    CASH = "Cash"
    CARD = "Card"
    UPI = "UPI"

class PaymentStatus(str, enum.Enum):
    PAID = "Paid"
    PENDING = "Pending"
    FAILED = "Failed"

class PhoneType(str, enum.Enum):
    MOBILE = "Mobile"
    HOME = "Home"
    WORK = "Work"
    OTHER = "Other"


class Hotel(Base):
    __tablename__ = "hotel"
    
    hotel_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False, unique=True)
    city = Column(String(100), nullable=False, index=True)
    address = Column(String(255))
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    employees = relationship("Employee", back_populates="hotel", cascade="all, delete-orphan")
    rooms = relationship("Room", back_populates="hotel", cascade="all, delete-orphan")


class Employee(Base):
    __tablename__ = "employee"
    
    emp_id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_id = Column(Integer, ForeignKey("hotel.hotel_id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    role = Column(String(100), index=True)
    salary = Column(DECIMAL(12, 2))
    hired_date = Column(Date)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    hotel = relationship("Hotel", back_populates="employees")


class Room(Base):
    __tablename__ = "room"
    
    room_id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_id = Column(Integer, ForeignKey("hotel.hotel_id", ondelete="CASCADE"), nullable=False, index=True)
    room_number = Column(String(20), nullable=False)
    room_type = Column(String(50), nullable=False, index=True)
    price_per_night = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum(RoomStatus), nullable=False, default=RoomStatus.AVAILABLE)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    __table_args__ = (
        Index('idx_room_hotel', 'hotel_id'),
        Index('uq_room_unique', 'hotel_id', 'room_number', unique=True),
    )
    
    # Relationships
    hotel = relationship("Hotel", back_populates="rooms")
    bookings = relationship("Booking", back_populates="room")


class Guest(Base):
    __tablename__ = "guest"
    
    guest_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False, index=True)
    email = Column(String(150), unique=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    phones = relationship("GuestPhone", back_populates="guest", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="guest")


class GuestPhone(Base):
    __tablename__ = "guest_phone"
    
    guest_id = Column(Integer, ForeignKey("guest.guest_id", ondelete="CASCADE"), primary_key=True)
    phone = Column(String(30), primary_key=True, index=True)
    phone_type = Column(Enum(PhoneType), default=PhoneType.MOBILE)
    
    # Relationships
    guest = relationship("Guest", back_populates="phones")


class Booking(Base):
    __tablename__ = "booking"
    
    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    guest_id = Column(Integer, ForeignKey("guest.guest_id", ondelete="RESTRICT"), nullable=False, index=True)
    room_id = Column(Integer, ForeignKey("room.room_id", ondelete="RESTRICT"), nullable=False, index=True)
    check_in_date = Column(Date, nullable=False)
    check_out_date = Column(Date, nullable=False)
    booking_date = Column(Date, nullable=False, server_default=func.current_date())
    status = Column(Enum(BookingStatus), nullable=False, default=BookingStatus.CONFIRMED)
    total_amount = Column(DECIMAL(12, 2), nullable=False, default=0.00)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    __table_args__ = (
        CheckConstraint('check_out_date > check_in_date', name='chk_dates'),
        Index('idx_booking_dates', 'check_in_date', 'check_out_date'),
    )
    
    # Relationships
    guest = relationship("Guest", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")
    payments = relationship("Payment", back_populates="booking", cascade="all, delete-orphan")
    service_usages = relationship("ServiceUsage", back_populates="booking", cascade="all, delete-orphan")


class Payment(Base):
    __tablename__ = "payment"
    
    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("booking.booking_id", ondelete="CASCADE"), nullable=False, index=True)
    payment_date = Column(Date, nullable=False, server_default=func.current_date())
    amount = Column(DECIMAL(12, 2), nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    payment_status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PAID, index=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    booking = relationship("Booking", back_populates="payments")


class Service(Base):
    __tablename__ = "service"
    
    service_id = Column(Integer, primary_key=True, autoincrement=True)
    service_name = Column(String(150), nullable=False, unique=True)
    price = Column(DECIMAL(10, 2), nullable=False, index=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    service_usages = relationship("ServiceUsage", back_populates="service")


class ServiceUsage(Base):
    __tablename__ = "service_usage"
    
    booking_id = Column(Integer, ForeignKey("booking.booking_id", ondelete="CASCADE"), primary_key=True)
    service_id = Column(Integer, ForeignKey("service.service_id", ondelete="RESTRICT"), primary_key=True, index=True)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    booking = relationship("Booking", back_populates="service_usages")
    service = relationship("Service", back_populates="service_usages")
