from exceptions.custom_exception import CustomException

# Users table:
# - userID: A unique Identification number for each user
# - username: The name of the user
# - password: The password of the user (hashed)
# - isAdmin: A boolean value to determine if the user is an admin

# Order table:
# - orderID: A unique Identification number for each order
# - userID: A unique Identification number for each user
# - bookID: A unique Identification number for each book/series
# - orderDate: The date when the order was made


# Create a new user in the database
def create_user(connection, username : str, password : str, isAdmin : bool) -> int:
    cursor = connection.cursor(dictionary=True)
    #check if user already exists
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
    if cursor.fetchone() is not None:
        raise CustomException("Username already exists")
    cursor.execute(
            """
            INSERT INTO users (username, password, isAdmin) 
            VALUES (%s, %s, %s)
            """, 
            (username, password, isAdmin)
        )
    connection.commit()
    return cursor.lastrowid

# Get a user from the database
def get_user(connection, userID : int) -> dict:
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM users WHERE userID = {userID}")
    return cursor.fetchone()

# Get all users from the database
def get_all_users(connection) -> list:
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Add an order to the database
def add_order(connection, userID : int, bookID : int, orderDate : str) -> int:
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
            """
            INSERT INTO orders (userID, bookID, orderDate) 
            VALUES (%s, %s, %s)
            """, 
            (userID, bookID, orderDate)
        )
    connection.commit()
    return cursor.lastrowid

# Get an order from the database
def get_order(connection, orderID : int) -> dict:
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM orders WHERE orderID = {orderID}")
    return cursor.fetchone()

# Get all orders from the database
def get_all_orders(connection) -> list:
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders")
    return cursor.fetchall()

# Login as a user
def login(connection, username : str, password : str) -> int:
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT userID FROM users WHERE username = '{username}' AND password = '{password}'")
    user = cursor.fetchone()
    if user is None:
        raise CustomException("Invalid username or password")
    return user['userID']