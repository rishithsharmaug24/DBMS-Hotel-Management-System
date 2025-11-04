"""
Hotel Management Database Connector
Connects frontend inputs to existing MySQL databases
Lightweight API layer without SQLAlchemy - uses raw SQL
"""

import mysql.connector
from mysql.connector import Error
from typing import Dict, List, Optional, Tuple, Any
from datetime import date, datetime
import json


class DatabaseConnector:
    """
    MySQL Database Connector
    Handles all database operations for existing hotel management tables
    """
    
    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306):
        """
        Initialize database connection
        
        Args:
            host: Database host (e.g., 'localhost')
            user: Database username
            password: Database password
            database: Database name
            port: Database port (default: 3306)
        """
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'port': port
        }
        self.connection = None
        self.connect()
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                print(f"✓ Connected to MySQL database: {self.config['database']}")
                return True
        except Error as e:
            print(f"✗ Database connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✓ Database connection closed")
    
    def execute_query(self, query: str, params: tuple = None) -> bool:
        """
        Execute INSERT, UPDATE, DELETE queries
        
        Args:
            query: SQL query string
            params: Query parameters (optional)
        
        Returns:
            bool: Success status
        """
        cursor = None
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return True
        except Error as e:
            print(f"✗ Query execution failed: {e}")
            self.connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
    
    def fetch_one(self, query: str, params: tuple = None) -> Optional[Dict]:
        """
        Fetch single row
        
        Args:
            query: SQL query string
            params: Query parameters (optional)
        
        Returns:
            Dict: Row as dictionary or None
        """
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            return result
        except Error as e:
            print(f"✗ Fetch failed: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    def fetch_all(self, query: str, params: tuple = None) -> List[Dict]:
        """
        Fetch multiple rows
        
        Args:
            query: SQL query string
            params: Query parameters (optional)
        
        Returns:
            List[Dict]: List of rows as dictionaries
        """
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            return results
        except Error as e:
            print(f"✗ Fetch failed: {e}")
            return []
        finally:
            if cursor:
                cursor.close()


class HotelDatabaseAPI:
    """
    High-level API for hotel management operations
    Maps frontend inputs to database queries
    """
    
    def __init__(self, db_connector: DatabaseConnector):
        """Initialize with database connector"""
        self.db = db_connector
    
    # ========================================================================
    # HOTEL OPERATIONS
    # ========================================================================
    
    def add_hotel(self, hotel_data: Dict) -> Dict:
        """
        Add new hotel from frontend
        
        Args:
            hotel_data: {'hotel_id': str, 'name': str, 'city': str, 'address': str}
        
        Returns:
            {'success': bool, 'message': str, 'data': dict}
        """
        query = """
            INSERT INTO hotel (hotel_id, name, city, address)
            VALUES (%s, %s, %s, %s)
        """
        params = (
            hotel_data['hotel_id'],
            hotel_data['name'],
            hotel_data['city'],
            hotel_data['address']
        )
        
        success = self.db.execute_query(query, params)
        return {
            'success': success,
            'message': 'Hotel added successfully' if success else 'Failed to add hotel',
            'data': hotel_data if success else None
        }
    
    def get_hotel(self, hotel_id: str) -> Dict:
        """Get hotel by ID"""
        query = "SELECT * FROM hotel WHERE hotel_id = %s"
        result = self.db.fetch_one(query, (hotel_id,))
        return {
            'success': result is not None,
            'data': result
        }
    
    def get_all_hotels(self) -> Dict:
        """Get all hotels"""
        query = "SELECT * FROM hotel"
        results = self.db.fetch_all(query)
        return {
            'success': True,
            'data': results,
            'count': len(results)
        }
    
    def update_hotel(self, hotel_id: str, update_data: Dict) -> Dict:
        """
        Update hotel information
        
        Args:
            hotel_id: Hotel ID
            update_data: {'name': str, 'city': str, 'address': str} (any combination)
        """
        # Build dynamic UPDATE query
        set_clauses = []
        params = []
        
        for key, value in update_data.items():
            if key in ['name', 'city', 'address']:
                set_clauses.append(f"{key} = %s")
                params.append(value)
        
        if not set_clauses:
            return {'success': False, 'message': 'No valid fields to update'}
        
        params.append(hotel_id)
        query = f"UPDATE hotel SET {', '.join(set_clauses)} WHERE hotel_id = %s"
        
        success = self.db.execute_query(query, tuple(params))
        return {
            'success': success,
            'message': 'Hotel updated successfully' if success else 'Failed to update hotel'
        }
    
    def delete_hotel(self, hotel_id: str) -> Dict:
        """Delete hotel"""
        query = "DELETE FROM hotel WHERE hotel_id = %s"
        success = self.db.execute_query(query, (hotel_id,))
        return {
            'success': success,
            'message': 'Hotel deleted successfully' if success else 'Failed to delete hotel'
        }
    
    # ========================================================================
    # EMPLOYEE OPERATIONS
    # ========================================================================
    
    def add_employee(self, employee_data: Dict) -> Dict:
        """
        Add employee from frontend
        
        Args:
            employee_data: {'emp_id': str, 'hotel_id': str, 'name': str, 
                           'role': str, 'salary': float}
        """
        query = """
            INSERT INTO employee (emp_id, hotel_id, name, role, salary)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            employee_data['emp_id'],
            employee_data['hotel_id'],
            employee_data['name'],
            employee_data['role'],
            employee_data['salary']
        )
        
        success = self.db.execute_query(query, params)
        return {
            'success': success,
            'message': 'Employee added successfully' if success else 'Failed to add employee',
            'data': employee_data if success else None
        }
    
    def get_employee(self, emp_id: str) -> Dict:
        """Get employee by ID"""
        query = "SELECT * FROM employee WHERE emp_id = %s"
        result = self.db.fetch_one(query, (emp_id,))
        return {
            'success': result is not None,
            'data': result
        }
    
    def get_hotel_employees(self, hotel_id: str) -> Dict:
        """Get all employees of a hotel"""
        query = "SELECT * FROM employee WHERE hotel_id = %s"
        results = self.db.fetch_all(query, (hotel_id,))
        return {
            'success': True,
            'data': results,
            'count': len(results)
        }
    
    def update_employee(self, emp_id: str, update_data: Dict) -> Dict:
        """Update employee information"""
        set_clauses = []
        params = []
        
        for key, value in update_data.items():
            if key in ['name', 'role', 'salary', 'hotel_id']:
                set_clauses.append(f"{key} = %s")
                params.append(value)
        
        if not set_clauses:
            return {'success': False, 'message': 'No valid fields to update'}
        
        params.append(emp_id)
        query = f"UPDATE employee SET {', '.join(set_clauses)} WHERE emp_id = %s"
        
        success = self.db.execute_query(query, tuple(params))
        return {
            'success': success,
            'message': 'Employee updated' if success else 'Update failed'
        }
    
    def delete_employee(self, emp_id: str) -> Dict:
        """Delete employee"""
        query = "DELETE FROM employee WHERE emp_id = %s"
        success = self.db.execute_query(query, (emp_id,))
        return {'success': success}
    
    # ========================================================================
    # GUEST OPERATIONS
    # ========================================================================
    
    def add_guest(self, guest_data: Dict) -> Dict:
        """
        Register guest from frontend
        
        Args:
            guest_data: {'guest_id': str, 'name': str, 'phone': str, 'email': str}
        """
        query = """
            INSERT INTO guest (guest_id, name, phone, email)
            VALUES (%s, %s, %s, %s)
        """
        params = (
            guest_data['guest_id'],
            guest_data['name'],
            guest_data['phone'],
            guest_data['email']
        )
        
        success = self.db.execute_query(query, params)
        return {
            'success': success,
            'message': 'Guest registered' if success else 'Registration failed',
            'data': guest_data if success else None
        }
    
    def get_guest(self, guest_id: str) -> Dict:
        """Get guest by ID"""
        query = "SELECT * FROM guest WHERE guest_id = %s"
        result = self.db.fetch_one(query, (guest_id,))
        return {'success': result is not None, 'data': result}
    
    def get_guest_by_email(self, email: str) -> Dict:
        """Get guest by email"""
        query = "SELECT * FROM guest WHERE email = %s"
        result = self.db.fetch_one(query, (email,))
        return {'success': result is not None, 'data': result}
    
    def update_guest(self, guest_id: str, update_data: Dict) -> Dict:
        """Update guest information"""
        set_clauses = []
        params = []
        
        for key, value in update_data.items():
            if key in ['name', 'phone', 'email']:
                set_clauses.append(f"{key} = %s")
                params.append(value)
        
        if not set_clauses:
            return {'success': False, 'message': 'No valid fields'}
        
        params.append(guest_id)
        query = f"UPDATE guest SET {', '.join(set_clauses)} WHERE guest_id = %s"
        
        success = self.db.execute_query(query, tuple(params))
        return {'success': success}
    
    # ========================================================================
    # ROOM OPERATIONS
    # ========================================================================
    
    def add_room(self, room_data: Dict) -> Dict:
        """
        Add room from frontend
        
        Args:
            room_data: {'room_id': str, 'hotel_id': str, 'room_type': str, 
                       'price_per_night': float, 'status': str}
        """
        query = """
            INSERT INTO room (room_id, hotel_id, room_type, price_per_night, status)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            room_data['room_id'],
            room_data['hotel_id'],
            room_data['room_type'],
            room_data['price_per_night'],
            room_data.get('status', 'available')
        )
        
        success = self.db.execute_query(query, params)
        return {'success': success, 'data': room_data if success else None}
    
    def get_room(self, room_id: str) -> Dict:
        """Get room by ID"""
        query = "SELECT * FROM room WHERE room_id = %s"
        result = self.db.fetch_one(query, (room_id,))
        return {'success': result is not None, 'data': result}
    
    def get_available_rooms(self, hotel_id: str, room_type: str = None) -> Dict:
        """Get available rooms"""
        if room_type:
            query = """
                SELECT * FROM room 
                WHERE hotel_id = %s AND status = 'available' AND room_type = %s
            """
            results = self.db.fetch_all(query, (hotel_id, room_type))
        else:
            query = "SELECT * FROM room WHERE hotel_id = %s AND status = 'available'"
            results = self.db.fetch_all(query, (hotel_id,))
        
        return {'success': True, 'data': results, 'count': len(results)}
    
    def update_room_status(self, room_id: str, status: str) -> Dict:
        """Update room status"""
        query = "UPDATE room SET status = %s WHERE room_id = %s"
        success = self.db.execute_query(query, (status, room_id))
        return {'success': success}
    
    # ========================================================================
    # BOOKING OPERATIONS
    # ========================================================================
    
    def create_booking(self, booking_data: Dict) -> Dict:
        """
        Create booking from frontend
        
        Args:
            booking_data: {'booking_id': str, 'guest_id': str, 'room_id': str,
                          'check_in_date': str/date, 'check_out_date': str/date,
                          'total_amount': float}
        """
        query = """
            INSERT INTO booking (booking_id, guest_id, room_id, check_in_date, 
                                check_out_date, total_amount)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            booking_data['booking_id'],
            booking_data['guest_id'],
            booking_data['room_id'],
            booking_data['check_in_date'],
            booking_data['check_out_date'],
            booking_data['total_amount']
        )
        
        success = self.db.execute_query(query, params)
        
        # Update room status to occupied if booking successful
        if success:
            self.update_room_status(booking_data['room_id'], 'occupied')
        
        return {
            'success': success,
            'message': 'Booking created' if success else 'Booking failed',
            'data': booking_data if success else None
        }
    
    def get_booking(self, booking_id: str) -> Dict:
        """Get booking with guest and room details"""
        query = """
            SELECT b.*, g.name as guest_name, g.email, g.phone,
                   r.room_type, r.price_per_night, h.name as hotel_name
            FROM booking b
            JOIN guest g ON b.guest_id = g.guest_id
            JOIN room r ON b.room_id = r.room_id
            JOIN hotel h ON r.hotel_id = h.hotel_id
            WHERE b.booking_id = %s
        """
        result = self.db.fetch_one(query, (booking_id,))
        return {'success': result is not None, 'data': result}
    
    def get_guest_bookings(self, guest_id: str) -> Dict:
        """Get all bookings for a guest"""
        query = """
            SELECT b.*, r.room_type, h.name as hotel_name
            FROM booking b
            JOIN room r ON b.room_id = r.room_id
            JOIN hotel h ON r.hotel_id = h.hotel_id
            WHERE b.guest_id = %s
        """
        results = self.db.fetch_all(query, (guest_id,))
        return {'success': True, 'data': results, 'count': len(results)}
    
    def checkout(self, booking_id: str) -> Dict:
        """Process checkout - make room available"""
        # Get room_id from booking
        booking = self.get_booking(booking_id)
        if not booking['success']:
            return {'success': False, 'message': 'Booking not found'}
        
        room_id = booking['data']['room_id']
        success = self.update_room_status(room_id, 'available')
        
        return {
            'success': success['success'],
            'message': 'Checkout completed' if success['success'] else 'Checkout failed'
        }
    
    # ========================================================================
    # PAYMENT OPERATIONS
    # ========================================================================
    
    def add_payment(self, payment_data: Dict) -> Dict:
        """
        Add payment from frontend
        
        Args:
            payment_data: {'payment_id': str, 'booking_id': str, 
                          'payment_date': str/date, 'amount': float, 'method': str}
        """
        query = """
            INSERT INTO payment (payment_id, booking_id, payment_date, amount, method)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            payment_data['payment_id'],
            payment_data['booking_id'],
            payment_data['payment_date'],
            payment_data['amount'],
            payment_data['method']
        )
        
        success = self.db.execute_query(query, params)
        return {'success': success, 'data': payment_data if success else None}
    
    def get_booking_payments(self, booking_id: str) -> Dict:
        """Get all payments for a booking"""
        query = "SELECT * FROM payment WHERE booking_id = %s"
        results = self.db.fetch_all(query, (booking_id,))
        return {'success': True, 'data': results}
    
    def get_payment_balance(self, booking_id: str) -> Dict:
        """Calculate remaining balance"""
        # Get booking total
        booking_query = "SELECT total_amount FROM booking WHERE booking_id = %s"
        booking = self.db.fetch_one(booking_query, (booking_id,))
        
        if not booking:
            return {'success': False, 'message': 'Booking not found'}
        
        # Get total paid
        payment_query = "SELECT SUM(amount) as total_paid FROM payment WHERE booking_id = %s"
        payment = self.db.fetch_one(payment_query, (booking_id,))
        
        total_amount = booking['total_amount']
        total_paid = payment['total_paid'] or 0
        balance = total_amount - total_paid
        
        return {
            'success': True,
            'total_amount': total_amount,
            'total_paid': total_paid,
            'balance': balance
        }
    
    # ========================================================================
    # SERVICE OPERATIONS
    # ========================================================================
    
    def add_service(self, service_data: Dict) -> Dict:
        """Add service"""
        query = """
            INSERT INTO service (service_id, service_name, price)
            VALUES (%s, %s, %s)
        """
        params = (
            service_data['service_id'],
            service_data['service_name'],
            service_data['price']
        )
        
        success = self.db.execute_query(query, params)
        return {'success': success, 'data': service_data if success else None}
    
    def get_all_services(self) -> Dict:
        """Get all services"""
        query = "SELECT * FROM service"
        results = self.db.fetch_all(query)
        return {'success': True, 'data': results}
    
    def add_service_to_booking(self, service_usage_data: Dict) -> Dict:
        """
        Add service to booking
        
        Args:
            service_usage_data: {'booking_id': str, 'service_id': str, 
                                'quantity': int, 'total_price': float}
        """
        query = """
            INSERT INTO service_usage (booking_id, service_id, quantity, total_price)
            VALUES (%s, %s, %s, %s)
        """
        params = (
            service_usage_data['booking_id'],
            service_usage_data['service_id'],
            service_usage_data['quantity'],
            service_usage_data['total_price']
        )
        
        success = self.db.execute_query(query, params)
        
        # Update booking total amount
        if success:
            update_query = """
                UPDATE booking 
                SET total_amount = total_amount + %s 
                WHERE booking_id = %s
            """
            self.db.execute_query(update_query, (
                service_usage_data['total_price'],
                service_usage_data['booking_id']
            ))
        
        return {'success': success}
    
    def get_booking_services(self, booking_id: str) -> Dict:
        """Get all services used in a booking"""
        query = """
            SELECT su.*, s.service_name, s.price as unit_price
            FROM service_usage su
            JOIN service s ON su.service_id = s.service_id
            WHERE su.booking_id = %s
        """
        results = self.db.fetch_all(query, (booking_id,))
        return {'success': True, 'data': results}


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("HOTEL DATABASE CONNECTOR - Example Usage")
    print("="*70)
    
    # Initialize database connection
    db = DatabaseConnector(
        host='localhost',
        user='root',
        password='your_password',  # Change this
        database='hotel_management',  # Your database name
        port=3306
    )
    
    # Initialize API
    api = HotelDatabaseAPI(db)
    
    # Example: Add hotel from frontend
    print("\n1. Adding Hotel...")
    result = api.add_hotel({
        'hotel_id': 'HTL001',
        'name': 'Grand Plaza',
        'city': 'Mumbai',
        'address': '123 Marine Drive'
    })
    print(f"Result: {result}")
    
    # Example: Get all hotels
    print("\n2. Getting All Hotels...")
    result = api.get_all_hotels()
    print(f"Found {result['count']} hotels")
    
    # Example: Add guest
    print("\n3. Adding Guest...")
    result = api.add_guest({
        'guest_id': 'GST001',
        'name': 'John Doe',
        'phone': '+91-9876543210',
        'email': 'john@email.com'
    })
    print(f"Result: {result}")
    
    # Example: Get available rooms
    print("\n4. Getting Available Rooms...")
    result = api.get_available_rooms('HTL001')
    print(f"Found {result['count']} available rooms")
    
    # Close connection
    db.disconnect()
    
    print("\n" + "="*70)
    print("✓ Example completed!")
    print("="*70)