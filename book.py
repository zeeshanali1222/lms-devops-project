"""
book.py - Group A: Book Module

Purpose: Define the structure of a book.
Responsibilities: Store book data (ISBN, title, author, copies).
"""


class Book:
    """Represents a single book title held by the library.

    Attributes:
        isbn (str): Unique identifier for the book.
        title (str): Title of the book.
        author (str): Author of the book.
        copies (int): Number of copies currently available.
    """

    def __init__(self, isbn, title, author, copies):
        """Initialize a Book instance.

        Args:
            isbn (str): Unique identifier for the book.
            title (str): Title of the book.
            author (str): Author of the book.
            copies (int): Number of copies available.
        """
        self.isbn = isbn
        self.title = title
        self.author = author
        self.copies = copies

    def is_available(self):
        """Return True if at least one copy of the book is available."""
        return self.copies > 0

    def __repr__(self):
        return (
            f"Book(isbn={self.isbn!r}, title={self.title!r}, "
            f"author={self.author!r}, copies={self.copies})"
        )

    def __str__(self):
        return f'"{self.title}" by {self.author} (ISBN: {self.isbn}) - {self.copies} copies'
