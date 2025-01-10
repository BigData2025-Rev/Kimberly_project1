from sql import load_data, connect
from sql.users import Users
from sql.books import Books
from display_data import *
from exceptions.custom_exception import CustomException
import datetime
import bcrypt

PAGING_SIZE = 15

# Connect to the database
(cursor, connection) = connect.connect()
print("Connected to the database")
#use the database
cursor.execute("USE project1")

book_manager = Books(connection)
user_manager = Users(connection)

# Load data into the database
load_data.load_data(connection, book_manager, force=False)
connection.commit()





#Create default admin user for testing
try:
    user_manager.create_user("admin", "admin", True)
except CustomException as e:
    pass
    

#Function to display a paged table
#data is the data to display, data_function is the function to get the data, and args are the arguments to pass to the function
def show_paged_table(data_function : callable, *args):
    start = 0
    limit = PAGING_SIZE

    while True:
        table = data_function(start, limit, *args)
        action = print_table_paged(table, has_next=True if len(table) == limit else False, has_prev=True if start > 0 else False)
        if action == 1:
            start += limit
        elif action == -1:
            start -= limit
        else:
            break
    


def order_book():
    book = None
    while book is None:
        bookId = input("Enter the book ID for the book you wish to order: ")
        try:
            bookId = int(bookId)
        except:
            print("Invalid input. Please enter a number")
            continue
        
        book = book_manager.get_book_by_id(bookId)
        if book is None:
            print("Book not found. Please enter a valid book ID")
    
    timestamp = datetime.datetime.now().date()
    print(f"Ordering book {book['title']}, price: {book['price']}")
    confirm = input("Confirm order? (y/n): ")
    if confirm.lower() == 'y':
        user_manager.add_order(user, book['bookID'], timestamp)
        print("Order placed successfully")
    else:
        print("Order cancelled")
    input("Press enter to return to menu")



def view_books():
    while True:
        selected = options_prompt(["View all Books", "Search for a Book", "View Book Details", "View Categories", "Search by Category", "Back"], "What would you like to do?")
        if selected == 0:
            show_paged_table(book_manager.get_all_books)
        elif selected == 1:
            title = input("Enter the title of the book you would like to search for: ")
            show_paged_table(book_manager.get_book_by_title, title)
        elif selected == 2:
            try:
                bookID = int(input("Enter the book ID: "))
            except:
                print("Invalid input. Please enter a number")
                return
            book = book_manager.get_book_by_id(bookID)
            if book is None:
                print("Book not found")
                input("Press enter to continue")
                continue
            print_book_table([book])
        elif selected == 3:
            show_paged_table(book_manager.get_all_categories)
        elif selected == 4:
            try:
                categoryID = int(input("Enter the category ID: "))
            except:
                print("Invalid input. Please enter a number")
                return
            show_paged_table(book_manager.get_books_by_category, categoryID)
        else:
            break

def view_orders(userID):
    show_paged_table(user_manager.get_all_user_orders, userID)

def manage_users(userID):
    options = ["View all users", "Add user", "Delete user", "Add Admin", "Back"]
    while True:
        selected = options_prompt(options, "Manage Users")
        if options[selected] == "View all users":
            show_paged_table(user_manager.get_all_users)
        elif options[selected] == "Add user":
            username = input("Enter the username: ")
            password = input("Enter the password: ")
            try:
                user_manager.create_user(username, password, False)
                print("User added successfully")
            except CustomException as e:
                print(e)
            input("Press enter to continue")
        elif options[selected] == "Delete user":
            id = int(input("Enter the user ID: "))
            if id == userID:
                print("You cannot delete yourself")
                input("Press enter to continue")
                continue
            count = user_manager.delete_user(id)
            if count == 0:
                print("User not found")
            else:
                print("User deleted successfully")
            input("Press enter to continue")
        elif options[selected] == "Add Admin":
            userID = int(input("Enter the user ID: "))
            try:
                user_manager.promote_user(userID)
                username = user_manager.get_user(userID)['username']
                print(f"{username} is now an admin")
            except CustomException as e:
                print(e)
            input("Press enter to continue")
        else:
            break

def manage_books():
    options = ["Add Book", "Remove Book", "Update Price", "Back"]
    while True:
        selected = options_prompt(options, "Manage Books")
        if options[selected] == "Add Book":
            path = input("Enter the path to the CSV file: ")
            try:
                load_data.add_data(path, connection, book_manager)
                print("Books added successfully")
            except FileNotFoundError as e:
                print(e)
            input("Press enter to continue")
        elif options[selected] == "Remove Book":
            try:
                bookID = int(input("Enter the book ID: "))
            except:
                print("Invalid input. Please enter a number.")
                continue
            rows = book_manager.delete_book(bookID)
            if rows == 0:
                print("Book not found")
            else:
                print("Book deleted successfully")
            print("Press enter to continue")
        elif options[selected] == "Update Price":
            try:
                bookID = int(input("Enter the book ID: "))
                price = float(input("Enter the new price: "))
            except:
                print("Invalid input. Please enter a number.")
                continue
            rows = book_manager.update_book_price(bookID, price)
            if rows == 0:
                print("Book not found")
            else:
                print("Price updated successfully")
            print("Press enter to continue")
        else:
            break



#Main logic
user = None

def admin_loop():
    options = ["View all orders", "Manage users", "Manage books", "Back"]
    while True:
        selected = options_prompt(options, "Admin Panel")
        if options[selected] == "View all orders":
            show_paged_table(user_manager.get_all_orders)
        elif options[selected] == "Manage users":
            manage_users(user)
        elif options[selected] == "Manage books":
            manage_books()
        else:
            break
    



while user is None:
    selected = options_prompt(["Login", "Register", "Exit"], "Welcome to the bookstore! \nPlease login or register to continue.")
    if selected == 0:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        try:
            user = user_manager.login(username, password)
        except CustomException as e:
            print(e)
            input("\nPress enter to try again")
            user = None
        
    elif selected == 1:
        username = input("Select a username: ")
        password = input("Enter a password: ")
        try:
            user = user_manager.create_user(username, password, False)
        except CustomException as e:
            print(e)
            input("\nPress enter to try again")
            user = None
    else:
        exit()

while True:
    #Create a separate admin prompt that additionally includes: view all users, view all orders, manage users, manage books
    options = ["Browse books", "View orders", "Order book", "Exit"]
    #selected = options_prompt(["Browse books", "View orders", "Order book", "Exit"], f"Welcome {user_manager.get_user(user)['username']}! What would you like to do?")
    if user_manager.get_user(user)['isAdmin']:
        options.insert(0, "View Admin Panel")

    selected = options_prompt(options, f"Welcome {user_manager.get_user(user)['username']}! What would you like to do?")
    if options[selected] == "View Admin Panel":
        admin_loop()
    elif options[selected] == "Exit":
        break
    elif options[selected] == "Browse books":
        view_books()
    elif options[selected] == "View orders":
        view_orders(user)
    elif options[selected] == "Order book":
        order_book()

connection.close()
