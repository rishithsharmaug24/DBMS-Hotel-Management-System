from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

# Hotel Schemas
class HotelBase(BaseModel):
    name: str = Field(..., max_length=150)
    city: str = Field(..., max_length=100)
    address: Optional[str] = Field(None, max_length=255)

class HotelCreate(HotelBase):
    pass

class HotelResponse(HotelBase):
    hotel_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Employee Schemas
class EmployeeBase(BaseModel):
    hotel_id: int
    name: str = Field(..., max_length=150)
    role: Optional[str] = Field(None, max_length=100)
    salary: Optional[Decimal] = None
    hired_date: Optional[date] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    emp_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Room Schemas
class RoomBase(BaseModel):
    hotel_id: int
    room_number: str = Field(..., max_length=20)
    room_type: str = Field(..., max_length=50)
    price_per_night: Decimal = Field(..., gt=0)
    status: str = "Available"

class RoomCreate(RoomBase):
    pass

class RoomResponse(RoomBase):
    room_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Guest Schemas
class GuestPhoneBase(BaseModel):
    phone: str = Field(..., max_length=30)
    phone_type: str = "Mobile"

class GuestBase(BaseModel):
    name: str = Field(..., max_length=150)
    email: Optional[EmailStr] = None

class GuestCreate(GuestBase):
    phones: Optional[List[GuestPhoneBase]] = []

class GuestResponse(GuestBase):
    guest_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Booking Schemas
class BookingBase(BaseModel):
    guest_id: int
    room_id: int
    check_in_date: date
    check_out_date: date
    status: str = "Confirmed"

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    status: Optional[str] = None
    check_in_date: Optional[date] = None
    check_out_date: Optional[date] = None

class BookingResponse(BookingBase):
    booking_id: int
    booking_date: date
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class BookingWithTotal(BookingResponse):
    total_amount: Optional[Decimal] = None


# Payment Schemas
class PaymentBase(BaseModel):
    booking_id: int
    amount: Decimal = Field(..., gt=0)
    payment_method: str
    payment_status: str = "Paid"

class PaymentCreate(PaymentBase):
    payment_date: Optional[date] = None

class PaymentResponse(PaymentBase):
    payment_id: int
    payment_date: date
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Service Schemas
class ServiceBase(BaseModel):
    service_name: str = Field(..., max_length=150)
    price: Decimal = Field(..., gt=0)

class ServiceCreate(ServiceBase):
    pass

class ServiceResponse(ServiceBase):
    service_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Service Usage Schemas
class ServiceUsageBase(BaseModel):
    booking_id: int
    service_id: int
    quantity: int = Field(default=1, gt=0)

class ServiceUsageCreate(ServiceUsageBase):
    pass

class ServiceUsageResponse(ServiceUsageBase):
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
