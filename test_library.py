"""
test_library.py - Group H: Unit Testing Module

Purpose: Ensure modules work correctly.
Responsibilities: Write tests for all major functions.

Run with: pytest test_library.py
"""

from book import Book
from member import Member
from library import Library
from issue_return import issue_book, return_book
from search import search_by_title, search_by_author, search_by_isbn
from auth_system import authenticate, register_user


# ---------- Book / Library tests ----------

def test_add_book():
    library = Library()
    book = Book('123', 'Test Book', 'Author', 2)
    library.add_book(book)
    assert '123' in library.books


def test_add_book_merges_existing_isbn():
    library = Library()
    library.add_book(Book('123', 'Test Book', 'Author', 2))
    library.add_book(Book('123', 'Test Book', 'Author', 3))
    assert library.books['123'].copies == 5


def test_remove_book():
    library = Library()
    library.add_book(Book('123', 'Test Book', 'Author', 2))
    assert library.remove_book('123') is True
    assert '123' not in library.books
    assert library.remove_book('999') is False


def test_list_books():
    library = Library()
    library.add_book(Book('1', 'A', 'Auth A', 1))
    library.add_book(Book('2', 'B', 'Auth B', 1))
    assert len(library.list_books()) == 2


# ---------- Member tests ----------

def test_member_borrow_and_return():
    member = Member('M1', 'Alice')
    member.borrow_book('123')
    assert '123' in member.borrowed_books
    assert member.return_book('123') is True
    assert '123' not in member.borrowed_books
    assert member.return_book('123') is False


# ---------- Issue / Return tests ----------

def test_issue_book_success():
    library = Library()
    library.add_book(Book('123', 'Test Book', 'Author', 1))
    member = Member('M1', 'Alice')
    assert issue_book(library, '123', member) is True
    assert library.books['123'].copies == 0
    assert '123' in member.borrowed_books


def test_issue_book_no_copies():
    library = Library()
    library.add_book(Book('123', 'Test Book', 'Author', 0))
    member = Member('M1', 'Alice')
    assert issue_book(library, '123', member) is False


def test_issue_book_not_found():
    library = Library()
    member = Member('M1', 'Alice')
    assert issue_book(library, '999', member) is False


def test_return_book_success():
    library = Library()
    library.add_book(Book('123', 'Test Book', 'Author', 1))
    member = Member('M1', 'Alice')
    issue_book(library, '123', member)
    assert return_book(library, '123', member) is True
    assert library.books['123'].copies == 1
    assert '123' not in member.borrowed_books


def test_return_book_not_borrowed():
    library = Library()
    library.add_book(Book('123', 'Test Book', 'Author', 1))
    member = Member('M1', 'Alice')
    assert return_book(library, '123', member) is False


# ---------- Search tests ----------

def test_search_by_title():
    library = Library()
    library.add_book(Book('1', 'Python Basics', 'Auth A', 1))
    library.add_book(Book('2', 'Advanced Python', 'Auth B', 1))
    results = search_by_title(library, 'python')
    assert len(results) == 2


def test_search_by_author():
    library = Library()
    library.add_book(Book('1', 'Book A', 'John Doe', 1))
    library.add_book(Book('2', 'Book B', 'Jane Smith', 1))
    results = search_by_author(library, 'john')
    assert len(results) == 1
    assert results[0].isbn == '1'


def test_search_by_isbn():
    library = Library()
    library.add_book(Book('123', 'Test Book', 'Author', 1))
    assert search_by_isbn(library, '123').title == 'Test Book'
    assert search_by_isbn(library, '999') is None


# ---------- Auth tests ----------

def test_authenticate_success():
    user_db = {'admin': 'password123'}
    assert authenticate('admin', 'password123', user_db) is True


def test_authenticate_failure():
    user_db = {'admin': 'password123'}
    assert authenticate('admin', 'wrongpass', user_db) is False
    assert authenticate('unknown', 'password123', user_db) is False


def test_register_user():
    user_db = {}
    assert register_user('newuser', 'pass', user_db) is True
    assert user_db['newuser'] == 'pass'
    assert register_user('newuser', 'other', user_db) is False
