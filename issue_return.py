"""
issue_return.py - Group D: Issue and Return Module

Purpose: Handle book issuance and return.
Responsibilities: Update availability when members borrow or return books.
"""


def issue_book(library, isbn, member):
    """Issue a book to a member if a copy is available.

    Args:
        library (Library): The library holding the book collection.
        isbn (str): ISBN of the book to issue.
        member (Member): The member borrowing the book.

    Returns:
        bool: True if the book was successfully issued, False otherwise
            (book not found or no copies available).
    """
    book = library.books.get(isbn)
    if book is not None and book.copies > 0:
        book.copies -= 1
        member.borrow_book(isbn)
        return True
    return False


def return_book(library, isbn, member):
    """Return a book previously issued to a member.

    Args:
        library (Library): The library holding the book collection.
        isbn (str): ISBN of the book being returned.
        member (Member): The member returning the book.

    Returns:
        bool: True if the return was processed successfully, False if the
            member did not have this book borrowed or the book does not
            exist in the library.
    """
    if isbn not in library.books:
        return False
    if member.return_book(isbn):
        library.books[isbn].copies += 1
        return True
    return False
