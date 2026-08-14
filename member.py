"""
member.py - Group B: Member Module

Purpose: Manage library members.
Responsibilities: Track member ID, name, and borrowed books.
"""


class Member:
    """Represents a library member.

    Attributes:
        member_id (str): Unique identifier for the member.
        name (str): Full name of the member.
        borrowed_books (list): List of ISBNs currently borrowed by the member.
    """

    def __init__(self, member_id, name):
        """Initialize a Member instance.

        Args:
            member_id (str): Unique identifier for the member.
            name (str): Full name of the member.
        """
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, isbn):
        """Record that this member has borrowed the given book (by ISBN)."""
        self.borrowed_books.append(isbn)

    def return_book(self, isbn):
        """Remove the given ISBN from this member's borrowed list, if present.

        Returns:
            bool: True if the book was found and removed, False otherwise.
        """
        if isbn in self.borrowed_books:
            self.borrowed_books.remove(isbn)
            return True
        return False

    def __repr__(self):
        return (
            f"Member(member_id={self.member_id!r}, name={self.name!r}, "
            f"borrowed_books={self.borrowed_books!r})"
        )

    def __str__(self):
        return f"Member {self.name} (ID: {self.member_id}) - {len(self.borrowed_books)} book(s) borrowed"
