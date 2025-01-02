from sql import load_data, connect

# Connect to the database
(cursor, connection) = connect.connect()
print("Connected to the database")
#use the database
cursor.execute("USE project1")

# Load data into the database
load_data.load_data(cursor, force=True)
connection.commit()

# print state of the database
cursor.execute("SELECT * FROM Books")
print(cursor.fetchall())

cursor.execute("SELECT * FROM Categories")
print(cursor.fetchall())

cursor.execute("SELECT * FROM BooksCategories")
print(cursor.fetchall())

cursor.close()


