# Kimberly_project1

To run project, create .env file in root directory with the following variables:
USER, PASSWORD, HOST
 
https://www.kaggle.com/datasets/elvinrustam/books-dataset?select=BooksDatasetClean.csv


SCHEMA
Books table:
- bookID: A unique Identification number for each book/series
- title: The name under which the book was published
- authors: Names of the authors of the book.
- description: A brief description of the book. May be null
- publisher: The publisher of the book
- startingPrice: The starting price of the book
- publishedMonth: The date when the book was published
- publishedYear: The date when the book was published

Categories table:
- categoryID: A unique Identification number for each category
- categoryName: The name of the category

BooksCategories table:
- bookID: A unique Identification number for each book/series
- categoryID: A unique Identification number for each category

Users table:
- userID: A unique Identification number for each user
- username: The name of the user
- password: The password of the user (hashed)
- isAdmin: A boolean value to determine if the user is an admin

Order table:
- orderID: A unique Identification number for each order
- userID: A unique Identification number for each user
- bookID: A unique Identification number for each book/series
- orderDate: The date when the order was made
