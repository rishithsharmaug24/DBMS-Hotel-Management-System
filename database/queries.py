# database/queries.py
"""
Database query functions for the Hotel Management System.
Handles dashboard data, recent bookings, and other queries.
"""

import pymysql
from config import settings


# -------------------------------------------------------------
# 🔌 Database Connection Helper
# -------------------------------------------------------------
def get_connection():
    """
    Establish a database connection using .env variables from config.py.
    Returns a connection object or None if connection fails.
    """
    try:
        conn = pymysql.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
            port=settings.DB_PORT,
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        print("❌ Database connection failed:", e)
        return None


# -------------------------------------------------------------
# 📊 Dashboard Stats
# -------------------------------------------------------------
def get_dashboard_stats():
    """
    Fetch summarized dashboard statistics from the database.
    Returns counts for rooms, guests, bookings, and revenue.
    """
    conn = get_connection()
    if not conn:
        return {
            "total_rooms": 0,
            "occupied": 0,
            "bookings_today": 0,
            "revenue_today": "₹0"
        }

    try:
        with conn.cursor() as cursor:
            # Total rooms
            cursor.execute("SELECT COUNT(*) AS total_rooms FROM rooms;")
            total_rooms = cursor.fetchone()["total_rooms"]

            # Occupied rooms
            cursor.execute("SELECT COUNT(*) AS occupied FROM rooms WHERE status='Occupied';")
            occupied = cursor.fetchone()["occupied"]

            # Bookings today
            cursor.execute("SELECT COUNT(*) AS bookings_today FROM bookings WHERE DATE(checkin_date)=CURDATE();")
            bookings_today = cursor.fetchone()["bookings_today"]

            # Revenue today
            cursor.execute("SELECT IFNULL(SUM(amount),0) AS revenue_today FROM payments WHERE DATE(payment_date)=CURDATE();")
            revenue_today = cursor.fetchone()["revenue_today"]

        return {
            "total_rooms": total_rooms,
            "occupied": occupied,
            "bookings_today": bookings_today,
            "revenue_today": f"₹{revenue_today:,}",
        }

    except Exception as e:
        print("❌ Query failed:", e)
        return {
            "total_rooms": 0,
            "occupied": 0,
            "bookings_today": 0,
            "revenue_today": "₹0",
        }
    finally:
        conn.close()


# -------------------------------------------------------------
# 🧾 Recent Bookings
# -------------------------------------------------------------
def get_recent_bookings(limit=5):
    """
    Fetch the most recent bookings for dashboard display.
    Returns a list of dicts with guest name, room, and status.
    """
    conn = get_connection()
    if not conn:
        return []

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    g.name AS guest_name,
                    r.room_number AS room_number,
                    b.status AS booking_status,
                    DATE_FORMAT(b.checkin_date, '%Y-%m-%d') AS checkin_date,
                    DATE_FORMAT(b.checkout_date, '%Y-%m-%d') AS checkout_date
                FROM bookings b
                JOIN guests g ON b.guest_id = g.guest_id
                JOIN rooms r ON b.room_id = r.room_id
                ORDER BY b.booking_date DESC
                LIMIT %s;
            """, (limit,))
            records = cursor.fetchall()
            return records

    except Exception as e:
        print("❌ Failed to fetch recent bookings:", e)
        return []
    finally:
        conn.close()


# -------------------------------------------------------------
# 🧪 Connection Test Helper (optional)
# -------------------------------------------------------------
def test_connection():
    """
    Simple test function to verify database connection.
    Returns True if connection is successful, False otherwise.
    """
    conn = get_connection()
    if conn:
        conn.close()
        print("✅ Database connection successful.")
        return True
    print("❌ Database connection failed.")
    return False


# -------------------------------------------------------------
# 🧭 Run manually for testing
# -------------------------------------------------------------
if __name__ == "__main__":
    print("Testing database queries...\n")
    test_connection()
    print("Dashboard Stats:", get_dashboard_stats())
    print("Recent Bookings:", get_recent_bookings())

