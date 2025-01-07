from sql import load_data, connect
from sql.users import Users
from sql.books import Books
from display_data import *
from exceptions.custom_exception import CustomException

PAGING_SIZE = 20

# Connect to the database
(cursor, connection) = connect.connect()
print("Connected to the database")
#use the database
cursor.execute("USE project1")

# Load data into the database
load_data.load_data(cursor)
connection.commit()

book_manager = Books(connection)
user_manager = Users(connection)

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
    pass

def view_books():
    selected = options_prompt(["View all books", "Search for a book", "View categories", "Search by category"], "What would you like to do?")
    if selected == 0:
        show_paged_table(book_manager.get_all_books)
    elif selected == 1:
        title = input("Enter the title of the book you would like to search for: ")
        books = book_manager.get_book_by_title(title)
        print_table(books)
    elif selected == 2:
        show_paged_table(book_manager.get_all_categories)
    elif selected == 3:
        categoryID = int(input("Enter the category ID: "))
        show_paged_table(book_manager.get_books_by_category, categoryID)
        pass

def view_orders():
    pass


#Main logic
user = None
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
    selected = options_prompt(["Browse books", "View orders", "Order book", "Exit"], f"Welcome {user_manager.get_user(user)['username']}! What would you like to do?")
    if selected == 0:
        view_books()
    elif selected == 1:
        pass
    elif selected == 2:
        pass
    else:
        break

connection.close()
