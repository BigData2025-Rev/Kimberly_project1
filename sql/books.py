# Books table:
# - bookID: A unique Identification number for each book/series
# - title: The name under which the book was published
# - authors: Names of the authors of the book.
# - description: A brief description of the book. May be null
# - publisher: The publisher of the book
# - startingPrice: The starting price of the book
# - publishedMonth: The date when the book was published
# - publishedYear: The date when the book was published

# Categories table:
# - categoryID: A unique Identification number for each category
# - categoryName: The name of the category

# BooksCategories table:
# - bookID: A unique Identification number for each book/series
# - categoryID: A unique Identification number for each category


#Searches for books in the dataset by title
def get_book_by_title(connection, title : str) -> dict:
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM books WHERE LOWER(title) LIKE LOWER(%s)"
    cursor.execute(query, (f"%{title}%",))
    return cursor.fetchall()

def get_category(connection, categoryID : int) -> dict:
    pass

#Used to return all books in the dataset
def get_all_books(connection, start : int = 0, limit : int = 20) -> list:
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM books LIMIT %s OFFSET %s"
    cursor.execute(query, (limit, start))
    return cursor.fetchall()

#Returns a table listing all categories + number of books, ordered by the # of books in each category
def get_all_categories(connection, start : int = 0, limit : int = 20) -> list:
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT Categories.categoryID, categoryName, COUNT(bookID) as bookCount
        FROM Categories
        JOIN BooksCategories ON Categories.categoryID = BooksCategories.categoryID
        GROUP BY Categories.categoryID
        ORDER BY bookCount DESC
        LIMIT %s OFFSET %s
        """,
        (limit, start)
    )
    return cursor.fetchall()

    

#Returns a table of books in a specific category
#Returns bookId, title, price, Categories
def get_books_by_category(connection, start : int, limit : int, categoryID : int) -> list:
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT Books.bookID, title, startingPrice, categoryName
        FROM Books
            JOIN BooksCategories ON Books.bookID = BooksCategories.bookID
            JOIN Categories ON BooksCategories.categoryID = Categories.categoryID
        WHERE Categories.categoryID = %s
        LIMIT %s OFFSET %s
        """,
        (categoryID, limit, start)
    )
    
    
    return cursor.fetchall()

def get_book_count(connection) -> int:
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as count FROM books")
    return cursor.fetchone()['count']


#To be implemented
def get_books_by_author(connection, author : str) -> list:
    pass

