"""
library.py - Group C: Library Module

Purpose: Manage the library's book collection.
Responsibilities: Add, remove, update, and list books.
"""


class Library:
    """Represents the library's collection of books.

    Attributes:
        books (dict): Mapping of ISBN (str) -> Book instance.
    """

    def __init__(self):
        """Initialize an empty library collection."""
        self.books = {}

    def add_book(self, book):
        """Add a Book instance to the library.

        If a book with the same ISBN already exists, its copy count is
        increased by the new book's copies instead of overwriting it.

        Args:
            book (Book): The book to add.
        """
        if book.isbn in self.books:
            self.books[book.isbn].copies += book.copies
        else:
            self.books[book.isbn] = book

    def remove_book(self, isbn):
        """Remove a book from the library by ISBN.

        Args:
            isbn (str): The ISBN of the book to remove.

        Returns:
            bool: True if the book was removed, False if it wasn't found.
        """
        if isbn in self.books:
            del self.books[isbn]
            return True
        return False

    def list_books(self):
        """Return a list of all Book instances in the library."""
        return list(self.books.values())

    def get_book(self, isbn):
        """Return the Book instance for a given ISBN, or None if not found."""
        return self.books.get(isbn)

    def __repr__(self):
        return f"Library(books={list(self.books.keys())!r})"
