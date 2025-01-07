import csv
import os

FILE_NAME = 'datafiles/bookstest.csv'


# Load data from a CSV file into an array
def read_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data

# Recreates the tables in the database
def create_tables(cursor):
    cursor.execute("DROP TABLE IF EXISTS Orders")
    cursor.execute("DROP TABLE IF EXISTS Users")
    cursor.execute("DROP TABLE IF EXISTS BooksCategories")
    cursor.execute("DROP TABLE IF EXISTS Books")
    cursor.execute("DROP TABLE IF EXISTS Categories")
    cursor.execute("CREATE TABLE IF NOT EXISTS Books (bookID INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), " \
                   "authors VARCHAR(255), description TEXT, publisher VARCHAR(255), " \
                   "startingPrice DECIMAL(10,2), publishedMonth VARCHAR(15), publishedYear INT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Categories (categoryID INT AUTO_INCREMENT PRIMARY KEY, categoryName VARCHAR(255))")
    cursor.execute("CREATE TABLE IF NOT EXISTS BooksCategories (bookID INT, categoryID INT, PRIMARY KEY (bookID, categoryID)," \
                   "FOREIGN KEY (bookID) REFERENCES Books(bookID), FOREIGN KEY (categoryID) REFERENCES Categories(categoryID))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Users (userID INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255), "\
                   "isAdmin BOOLEAN)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Orders (orderID INT AUTO_INCREMENT PRIMARY KEY, userID INT, bookID INT, orderDate DATE, " \
                   "FOREIGN KEY (userID) REFERENCES Users(userID), FOREIGN KEY (bookID) REFERENCES Books(bookID))")

# Load data from the CSV file and add to database if the database is empty.
# If force is specified, will remove all data and reload it.
def load_data(cursor, force=False):
    if not force:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        if len(tables) > 0:
            return

    data = read_csv(FILE_NAME)
    create_tables(cursor)
    for row in data[1:]:
        if row[2] == '':
            row[2] = 'description not available'
        book_id = add_book(cursor, {'title': row[0], 'authors': row[1], 'description': row[2], 'publisher': row[4], 
                          'startingPrice': row[5], 'publishedMonth': row[6], 'publishedYear': row[7]})
        categories = row[3].split(',')
        categories = [category.strip() for category in categories]
        if len(categories) == 0:
            categories = ['Other']
        for category in categories:
            cursor.execute(f"SELECT categoryID FROM Categories WHERE categoryName = '{category}'")
            cat = cursor.fetchone()
            if cat is None:
                cursor.execute(f"INSERT INTO Categories (categoryName) VALUES ('{category}')")
                categoryID = cursor.lastrowid
            else:
                categoryID = cat[0]
            cursor.execute(f"INSERT INTO BooksCategories (bookID, categoryID) VALUES ('{book_id}', '{categoryID}')")
    

#Adds a book to the database
def add_book(cursor, book : dict) -> int:
    cursor.execute(
            """
            INSERT INTO books (title, authors, description, publisher, startingPrice, publishedMonth, publishedYear) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, 
            (book['title'], book['authors'], book['description'], book['publisher'], book['startingPrice'], book['publishedMonth'], book['publishedYear'])
        )
    return cursor.lastrowid
    
