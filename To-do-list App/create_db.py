import mysql.connector

dbConnection = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '199920'
)
cursor = dbConnection.cursor()

# Create database
cursor.execute("CREATE DATABASE IF NOT EXISTS todo_app")
cursor.execute("SHOW DATABASES")

# Consume the results from SHOW DATABASES to avoid "Unread result found" error
databases = cursor.fetchall()

# Switch to the new database
cursor.execute("USE todo_app")

# Create table
cursor.execute("CREATE TABLE Tasks(ID INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100), done BOOLEAN DEFAULT FALSE)")
print("Database and table created successfully!")

cursor.close()
dbConnection.close()