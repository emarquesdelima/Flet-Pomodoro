import mysql.connector
import os

host = "emarques.mysql.pythonanywhere-services.com"
user = "emarques"
# Fetching password from environment variable
password = os.environ.get('DB_PASSWORD')
db = "emarques$taskito"

# Using mysql.connector to establish a connection
connection = mysql.connector.connect(
    host=host, user=user, password=password, database=db)

# Your code here

# Ensure to close the connection
connection.close()
