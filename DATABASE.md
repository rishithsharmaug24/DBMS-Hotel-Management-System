# Database Documentation

## Overview
The Hotel Management System uses MySQL as its database backend, with multiple layers of abstraction:
- Raw SQL files for schema definition and initialization
- SQLAlchemy ORM for modern Python database interactions
- Direct MySQL connector for lightweight operations

## Database Configuration

### Connection Settings
The database connection is configured in `config.py`:
```python
DB_HOST: localhost
DB_PORT: 3306
DB_USER: root
DB_PASSWORD: (configured in .env or config.py)
DB_NAME: hotel_management_system
```

### Connection Methods

1. **SQLAlchemy ORM** (Primary method)
   - Used in `database.py` for the main application
   - Provides full ORM capabilities and session management
   - Connection URL: `mysql+pymysql://{user}:{password}@{host}:{port}/{database}`

2. **Direct MySQL Connector** (Secondary method)
   - Used in `hotel_management_system.py` for lightweight operations
   - Direct SQL execution without ORM overhead

## Database Schema

### Core Tables

1. **Hotel** (`hotel` table)
   - Primary hotel information
   - Relationships: employees, rooms
   - Key fields: hotel_id, name, city, address

2. **Employee** (`employee` table)
   - Staff management
   - Connected to hotels
   - Key fields: emp_id, hotel_id, name, role, salary

3. **Room** (`room` table)
   - Room inventory
   - Connected to hotels
   - Key fields: room_id, hotel_id, room_number, room_type, price_per_night

4. **Guest** (`guest` table)
   - Customer information
   - Has associated phone numbers
   - Key fields: guest_id, name, email

5. **Booking** (`booking` table)
   - Reservation management
   - Links guests, rooms, and services
   - Key fields: booking_id, guest_id, room_id, check_in_date, check_out_date

6. **Payment** (`payment` table)
   - Financial transactions
   - Connected to bookings
   - Key fields: payment_id, booking_id, amount, payment_method, status

7. **Service** (`service` table)
   - Additional hotel services
   - Key fields: service_id, service_name, price

### Supporting Tables

1. **GuestPhone** (`guest_phone` table)
   - Multiple phone numbers per guest
   - Key fields: guest_id, phone, phone_type

2. **ServiceUsage** (`service_usage` table)
   - Tracks services used in bookings
   - Key fields: booking_id, service_id, quantity

## Database Initialization

### Setup Process
The database is initialized through `setup_database()` in `database.py`, which runs SQL files in this order:

1. `database.sql` - Creates the database
2. `tables.sql` - Defines table structures
3. `views.sql` - Creates database views
4. `procedures.sql` - Defines stored procedures
5. `triggers.sql` - Sets up database triggers
6. `sample_data.sql` - (Optional) Adds sample data

### Running the Setup
```python
from database import setup_database
setup_database()  # Initializes complete database structure
```

## ORM Models

The system uses SQLAlchemy ORM models defined in `models.py`:

- Each table has a corresponding model class
- Models include relationship definitions
- Automatic timestamp handling for created_at/updated_at
- Foreign key constraints and cascading deletes where appropriate

## API Layer

### FastAPI Integration
- RESTful API endpoints in `main.py`
- Uses Pydantic models for request/response validation
- Automatic OpenAPI documentation

### Database Operations
CRUD operations are implemented in `crud.py`:
- Create: `create_*` functions
- Read: `get_*` functions
- Update: `update_*` functions
- Delete: `delete_*` functions

## Working with the Database

### Adding New Records
```python
from crud import create_hotel
from schemas import HotelCreate

new_hotel = HotelCreate(
    name="Grand Hotel",
    city="New York",
    address="123 Main St"
)
db_hotel = create_hotel(db, new_hotel)
```

### Querying Records
```python
from crud import get_hotel, get_hotels

# Get single hotel
hotel = get_hotel(db, hotel_id=1)

# Get all hotels
hotels = get_hotels(db)
```

### Making Bookings
```python
from crud import create_booking
from schemas import BookingCreate

new_booking = BookingCreate(
    guest_id=1,
    room_id=1,
    check_in_date="2025-11-01",
    check_out_date="2025-11-05"
)
booking = create_booking(db, new_booking)
```

## Database Maintenance

### Backup
The `database/backup/` directory is available for database backups.

### Sample Data
Sample data can be loaded from `database/sample_data/sample_data.sql`

## Error Handling

The system includes comprehensive error handling:
- Database connection errors
- Constraint violations
- Transaction management
- Automatic rollbacks on failure

## Security Considerations

1. Password Protection
   - Database passwords should be stored in environment variables
   - Use `.env` file for local development
   - Production credentials should be securely managed

2. SQL Injection Prevention
   - ORM uses parameterized queries
   - Direct SQL execution is properly escaped
   - Input validation through Pydantic models

3. Access Control
   - Session management
   - Role-based access control
   - Transaction isolation

## Performance Optimization

1. **Indexes** are defined in `database/schema/indexes.sql`
2. **Views** optimize common queries
3. Connection pooling is enabled
4. Prepared statements are used where possible

## Common Operations

### Check Room Availability
```python
from crud import get_available_rooms
from datetime import date

available_rooms = get_available_rooms(
    db,
    hotel_id=1,
    check_in=date(2025, 11, 1),
    check_out=date(2025, 11, 5)
)
```

### Process Payment
```python
from crud import create_payment
from schemas import PaymentCreate

payment = PaymentCreate(
    booking_id=1,
    amount=500.00,
    payment_method="CREDIT_CARD"
)
db_payment = create_payment(db, payment)
```

## Troubleshooting

1. **Connection Issues**
   - Verify database service is running
   - Check credentials in config.py or .env
   - Ensure proper network access

2. **Migration Issues**
   - Run setup_database() for clean installation
   - Check SQL file execution order
   - Verify file permissions

3. **Performance Issues**
   - Check query execution plans
   - Verify index usage
   - Monitor connection pool status