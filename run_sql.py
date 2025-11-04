import mysql.connector

# 1️⃣ Connect to your MySQL database
conn = mysql.connector.connect(
    host='localhost',         # or your database host
    user='root',              # your MySQL username
    password='your_password', # your MySQL password
    database='your_database'  # the database where you want to run the SQL
)

cursor = conn.cursor()

# 2️⃣ Read the SQL file
with open('hotel_management_system.sql', 'r') as file:
    sql_script = file.read()

# 3️⃣ Split and execute each statement
for statement in sql_script.split(';'):
    if statement.strip():  # ignore empty lines
        cursor.execute(statement)

# 4️⃣ Save changes and close connection
conn.commit()
cursor.close()
conn.close()

print("✅ SQL file executed successfully!")