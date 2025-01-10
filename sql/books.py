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
        self.connection = connection

    # Searches for books in the dataset by title
    def get_book_by_title(self, start: int, limit: int, title: str) -> dict:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT bookID, title, authors FROM books
            WHERE title LIKE %s
            LIMIT %s OFFSET %s
            """,
            (f"%{title}%", limit, start)
        )
        return cursor.fetchall()

    # Returns all books in the dataset, ordered alphabetically by title
    def get_all_books(self, start: int = 0, limit: int = 20) -> list:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT bookId, title, authors FROM books
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
            SELECT Books.bookID, title, authors, categoryName
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
    
    # Returns a book by its ID + category
    def get_book_by_id(self, bookID: int) -> dict:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT Books.bookID, title, authors, description, publisher, startingPrice as price, publishedMonth as pubMonth, publishedYear as pubYear, GROUP_CONCAT(categoryName SEPARATOR ', ') as categories
            FROM Books
            JOIN BooksCategories ON Books.bookID = BooksCategories.bookID
            JOIN Categories ON BooksCategories.categoryID = Categories.categoryID
            WHERE Books.bookID = %s
            """,
            (bookID,)
        )
        results = cursor.fetchall()
        if not results or len(results) == 0 or results[0]['bookID'] is None:
            return None
        
        return results[0]

    # Add category
    def add_category(self, category: str) -> int:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("INSERT INTO Categories (categoryName) VALUES (%s)", (category,))
        self.connection.commit()
        return cursor.lastrowid
    
    #Get category by name
    def get_category_by_name(self, category: str) -> dict:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Categories WHERE categoryName = %s", (category,))
        return cursor.fetchone()
    
    #Adds a relationship between a book and a category
    def add_book_category(self, bookID: int, categoryID: int):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("INSERT INTO BooksCategories (bookID, categoryID) VALUES (%s, %s)", (bookID, categoryID))
        self.connection.commit()
        return cursor.lastrowid

    # Adds a book to the database
    def add_book(self, book: dict) -> int:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(
            """
            INSERT INTO books (title, authors, description, publisher, startingPrice, publishedMonth, publishedYear) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (book['title'], book['authors'], book['description'], book['publisher'], book['startingPrice'], book['publishedMonth'], book['publishedYear'])
        )
        self.connection.commit()
        return cursor.lastrowid

    
    # Deletes a book from the database
    def delete_book(self, bookID: int):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("DELETE FROM books WHERE bookID = %s", (bookID,))
        self.connection.commit()

    # Updates the details of a book in the database
    def update_book(self, bookID: int, new_price: float):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("UPDATE books SET startingPrice = %s WHERE bookID = %s", (new_price, bookID))
        self.connection.commit()
        return cursor.rowcount


