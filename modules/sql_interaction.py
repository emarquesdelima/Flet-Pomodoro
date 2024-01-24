import pymysql
import os

host = "emarques.mysql.pythonanywhere-services.com"
user = "emarques"
# Fetching password from environment variable
password = os.environ.get('DB_PASSWORD')
db = "emarques$taskito"

connection = pymysql.connect(host=host, user=user, password=password, db=db)

# Your code here

connection.close()
