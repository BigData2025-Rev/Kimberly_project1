import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# Create a connection to the database, and create the database if it doesn't exist
def connect() -> mysql.connector.connection.MySQLConnection:
    connection = mysql.connector.connect(
        host=os.getenv('HOST'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
    )

    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS project1")
    cursor.close()
    connection.close()

    connection = mysql.connector.connect(
        host=os.getenv('HOST'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
        database='project1'
    )

    cursor = connection.cursor()
    return cursor, connection
