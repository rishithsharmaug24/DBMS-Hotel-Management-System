import mysql.connector
from mysql.connector import Error

def get_connection():
    """Establish a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",         # or your DB host
            user="root",              # change to your MySQL username
            password="your_password", # change this
            database="hotel_management_system"  # must match 01_create_database.sql
        )
        return connection
    except Error as e:
        print(f"❌ Database connection error: {e}")
        return None
