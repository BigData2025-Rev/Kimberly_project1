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


class Books:
    def __init__(self, connection):
        # Store the database connection as a class variable
        self.connection = connection

    # Searches for books in the dataset by title
    def get_book_by_title(self, title: str) -> dict:
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM books WHERE LOWER(title) LIKE LOWER(%s)"
        cursor.execute(query, (f"%{title}%",))
        return cursor.fetchall()

    # Returns all books in the dataset, ordered alphabetically by title
    def get_all_books(self, start: int = 0, limit: int = 20) -> list:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT * FROM books
            ORDER BY title
            LIMIT %s OFFSET %s
            """,
            (limit, start)
        )
        return cursor.fetchall()

    # Returns a table listing all categories + number of books, ordered by the number of books in each category
    def get_all_categories(self, start: int = 0, limit: int = 20) -> list:
        cursor = self.connection.cursor(dictionary=True)
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

    # Returns a table of books in a specific category
    # Returns bookId, title, price, and categoryName
    def get_books_by_category(self, start: int, limit: int, categoryID: int) -> list:
        cursor = self.connection.cursor(dictionary=True)
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

    # Returns the total count of books in the dataset
    def get_book_count(self) -> int:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as count FROM books")
        return cursor.fetchone()['count']


#To be implemented
def get_books_by_author(connection, author : str) -> list:
    pass

