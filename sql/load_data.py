import csv
import os
from mysql.connector.errors import IntegrityError
import logging

FILE_NAME = 'bookstest.csv'
ENCODING = 'utf-8'


# Load data from a CSV file into an array
def read_csv(file_path):
    with open('datafiles/' + file_path, 'r', encoding=ENCODING) as file:
        reader = csv.reader(file)
        data = list(reader)
    return data

# Recreates the tables in the database
def create_tables(cursor):
    logging.info("Creating tables")
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
                   "FOREIGN KEY (bookID) REFERENCES Books(bookID) ON DELETE CASCADE, FOREIGN KEY (categoryID) REFERENCES Categories(categoryID))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Users (userID INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255), "\
                   "isAdmin BOOLEAN)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Orders (orderID INT AUTO_INCREMENT PRIMARY KEY, userID INT, bookID INT, orderDate DATE, " \
                   "FOREIGN KEY (userID) REFERENCES Users(userID) ON DELETE SET NULL, FOREIGN KEY (bookID) REFERENCES Books(bookID) ON DELETE SET NULL)")

# Add data from a CSV file to the database
def add_data(csv_path, books):
    data = read_csv(csv_path)
    for row in data[1:]:
        if row[2] == '':
            row[2] = 'description not available'
        book_id = books.add_book({'title': row[0], 'authors': row[1], 'description': row[2], 'publisher': row[4], 
                          'startingPrice': row[5], 'publishedMonth': row[6], 'publishedYear': row[7]})
        
        if not row[3]:
            categories = ['Other']
        else:
            categories = row[3].split(',')
            categories = [category.strip() for category in categories]
        for category in categories:
            try:
                cat = books.get_category_by_name(category)
                if cat is None:
                    categoryID = books.add_category(category)
                else:
                    categoryID = cat['categoryID']
                books.add_book_category(book_id, categoryID)
            except IntegrityError as e:
                logging.error(f"Error adding book relation {row[0]}: {e}")

# Load data from the CSV file and add to database if the database is empty.
# If force is specified, will remove all data and reload it.
def load_data(connection, books, force=False):
    cursor = connection.cursor()
    if not force:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        if len(tables) > 0:
            return

    logging.info("Beginning data load")
    create_tables(cursor)
    add_data(FILE_NAME, books)
    
