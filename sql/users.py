from exceptions.custom_exception import CustomException
import bcrypt

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


class Users:
    def __init__(self, connection):
        self.connection = connection

    # Create a new user in the database
    def create_user(self, username: str, password: str, is_admin: bool) -> int:
        cursor = self.connection.cursor(dictionary=True)
        hashed_password = self.hash_password(password)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone() is not None:
            raise CustomException("Username already exists")
        cursor.execute(
            """
            INSERT INTO users (username, password, isAdmin) 
            VALUES (%s, %s, %s)
            """,
            (username, hashed_password, is_admin),
        )
        self.connection.commit()
        return cursor.lastrowid

    # Get a user from the database
    def get_user(self, user_id: int) -> dict:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE userID = %s", (user_id,))
        return cursor.fetchone()

    # Get all users from the database
    def get_all_users(self, start : int, limit : int) -> list:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT * FROM users
            LIMIT %s OFFSET %s
            """,
            (limit, start)
        )
        return cursor.fetchall()

    # Add an order to the database
    def add_order(self, user_id: int, book_id: int, order_date: str) -> int:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(
            """
            INSERT INTO orders (userID, bookID, orderDate) 
            VALUES (%s, %s, %s)
            """,
            (user_id, book_id, order_date),
        )
        self.connection.commit()
        return cursor.lastrowid

    # Get an order from the database
    def get_order(self, order_id: int) -> dict:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders WHERE orderID = %s", (order_id,))
        return cursor.fetchone()

    # Get all orders for a particular user, returning book name, order date, and order ID
    def get_all_user_orders(self, start : int, limit : int, userID : int) -> list:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT Orders.orderID, Books.title, Orders.orderDate
            FROM Orders
            JOIN Books ON Orders.bookID = Books.bookID
            WHERE Orders.userID = %s
            LIMIT %s OFFSET %s
            """,
            (userID, limit, start)
        )
        return cursor.fetchall()
    
    # Get all orders, orderID, userName, bookName, orderDate
    def get_all_orders(self, start : int, limit : int) -> list:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT Orders.orderID, COALESCE(Users.username, 'deleted user') AS username, COALESCE(Books.title, 'Book not available') AS title, Orders.orderDate
            FROM Orders
            LEFT JOIN Users ON Orders.userID = Users.userID
            LEFT JOIN Books ON Orders.bookID = Books.bookID
            LIMIT %s OFFSET %s
            """,
            (limit, start)
        )
        return cursor.fetchall()

    # Login as a user
    def login(self, username: str, password: str) -> int:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT userID, password FROM users WHERE username = %s",
            (username,),
        )
        user = cursor.fetchone()
        if user is None:
            raise CustomException("Invalid username or password")
        if not self.verify_password(password, user["password"]):
            raise CustomException("Invalid username or password")   
        return user["userID"]
    
    # Promotes a user to admin
    def promote_user(self, userID: int):
        cursor = self.connection.cursor(dictionary=True)
        user = self.get_user(userID)
        if user is None:
            raise CustomException("User not found")
        elif user["isAdmin"]:
            raise CustomException("User is already an admin")
        cursor.execute("UPDATE users SET isAdmin = 1 WHERE userID = %s", (userID,))
        self.connection.commit()

    # Deletes a user from the database
    def delete_user(self, userID: int):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("DELETE FROM users WHERE userID = %s", (userID,))
        self.connection.commit()
        return cursor.rowcount


    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))