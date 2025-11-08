from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import date

import importlib
import sys

# Force reload schemas module
if 'schemas' in sys.modules:
    importlib.reload(sys.modules['schemas'])
    
import models, schemas, crud
from database import engine, get_db
from config import settings

# Create tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="Complete Hotel Management System API"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============= HOTEL ENDPOINTS =============
@app.post("/hotels/", response_model=schemas.HotelResponse, status_code=status.HTTP_201_CREATED)
def create_hotel(hotel: schemas.HotelCreate, db: Session = Depends(get_db)):
    return crud.create_hotel(db, hotel)

@app.get("/hotels/", response_model=List[schemas.HotelResponse])
def read_hotels(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_hotels(db, skip, limit)

@app.get("/hotels/{hotel_id}", response_model=schemas.HotelResponse)
def read_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = crud.get_hotel(db, hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel

@app.put("/hotels/{hotel_id}", response_model=schemas.HotelResponse)
def update_hotel(hotel_id: int, hotel: schemas.HotelCreate, db: Session = Depends(get_db)):
    updated = crud.update_hotel(db, hotel_id, hotel)
    if not updated:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return updated

@app.delete("/hotels/{hotel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    if not crud.delete_hotel(db, hotel_id):
        raise HTTPException(status_code=404, detail="Hotel not found")


# ============= EMPLOYEE ENDPOINTS =============
@app.post("/employees/", response_model=schemas.EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db, employee)

@app.get("/employees/{emp_id}", response_model=schemas.EmployeeResponse)
def read_employee(emp_id: int, db: Session = Depends(get_db)):
    employee = crud.get_employee(db, emp_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.get("/hotels/{hotel_id}/employees", response_model=List[schemas.EmployeeResponse])
def read_hotel_employees(hotel_id: int, db: Session = Depends(get_db)):
    return crud.get_employees_by_hotel(db, hotel_id)


# ============= ROOM ENDPOINTS =============
@app.post("/rooms/", response_model=schemas.RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    return crud.create_room(db, room)

@app.get("/rooms/{room_id}", response_model=schemas.RoomResponse)
def read_room(room_id: int, db: Session = Depends(get_db)):
    room = crud.get_room(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@app.get("/hotels/{hotel_id}/available-rooms", response_model=List[schemas.RoomResponse])
def get_available_rooms(
    hotel_id: int, 
    check_in: date, 
    check_out: date, 
    db: Session = Depends(get_db)
):
    return crud.get_available_rooms(db, hotel_id, check_in, check_out)


# ============= GUEST ENDPOINTS =============
@app.post("/guests/", response_model=schemas.GuestResponse, status_code=status.HTTP_201_CREATED)
def create_guest(guest: schemas.GuestCreate, db: Session = Depends(get_db)):
    return crud.create_guest(db, guest)

@app.get("/guests/{guest_id}", response_model=schemas.GuestResponse)
def read_guest(guest_id: int, db: Session = Depends(get_db)):
    guest = crud.get_guest(db, guest_id)
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    return guest

@app.get("/guests/search/{search_term}", response_model=List[schemas.GuestResponse])
def search_guests(search_term: str, db: Session = Depends(get_db)):
    return crud.search_guests(db, search_term)


# ============= BOOKING ENDPOINTS =============
@app.post("/bookings/", response_model=schemas.BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    return crud.create_booking(db, booking)

@app.get("/bookings/{booking_id}", response_model=schemas.BookingResponse)
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = crud.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@app.get("/guests/{guest_id}/bookings", response_model=List[schemas.BookingResponse])
def read_guest_bookings(guest_id: int, db: Session = Depends(get_db)):
    return crud.get_bookings_by_guest(db, guest_id)


# ============= PAYMENT ENDPOINTS =============
@app.post("/payments/", response_model=schemas.PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    return crud.create_payment(db, payment)

@app.get("/bookings/{booking_id}/payments", response_model=List[schemas.PaymentResponse])
def read_booking_payments(booking_id: int, db: Session = Depends(get_db)):
    return crud.get_payments_by_booking(db, booking_id)


# ============= SERVICE ENDPOINTS =============
@app.post("/services/", response_model=schemas.ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service(service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    return crud.create_service(db, service)

@app.get("/services/", response_model=List[schemas.ServiceResponse])
def read_services(db: Session = Depends(get_db)):
    return crud.get_services(db)

@app.post("/bookings/{booking_id}/services", response_model=schemas.ServiceUsageResponse)
def add_service_to_booking(
    booking_id: int,
    service_usage: schemas.ServiceUsageCreate,
    db: Session = Depends(get_db)
):
    return crud.add_service_to_booking(db, service_usage)


# ============= ROOT ENDPOINT =============
@app.get("/")
def root():
    return {
        "message": "Hotel Management System API",
        "version": settings.API_VERSION,
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)