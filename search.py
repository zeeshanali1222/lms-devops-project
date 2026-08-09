"""
search.py - Group E: Search Module

Purpose: Enable search by title, author, or ISBN.
Responsibilities: Help users find available books.
"""


def search_by_title(library, title):
    """Search for books whose title contains the given substring (case-insensitive).

    Args:
        library (Library): The library to search.
        title (str): Substring to match against book titles.

    Returns:
        list[Book]: Matching books.
    """
    return [book for book in library.books.values() if title.lower() in book.title.lower()]


def search_by_author(library, author):
    """Search for books whose author contains the given substring (case-insensitive).

    Args:
        library (Library): The library to search.
        author (str): Substring to match against book authors.

    Returns:
        list[Book]: Matching books.
    """
    return [book for book in library.books.values() if author.lower() in book.author.lower()]


def search_by_isbn(library, isbn):
    """Search for a book by exact ISBN match.

    Args:
        library (Library): The library to search.
        isbn (str): ISBN to look up.

    Returns:
        Book | None: The matching book, or None if not found.
    """
    return library.books.get(isbn)
