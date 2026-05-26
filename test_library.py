import unittest
import os
import json
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.book import Book
from models.user import User, Member, Admin
from models.transaction import BorrowRecord
from utils.validators import is_valid_name, is_positive_int, is_valid_membership


class TestBook(unittest.TestCase):
    def test_book_creation(self):
        book = Book(1, "Clean Code", "Robert Martin")
        assert book.book_id == 1
        assert book.title == "Clean Code"
        assert book.available is True

    def test_book_availability_toggle(self):
        book = Book(1, "Test Book", "Author")
        book.available = False
        assert book.available is False

    def test_book_to_dict(self):
        book = Book(1, "Test", "Author", True)
        d = book.to_dict()
        assert d["id"] == 1
        assert d["available"] is True


class TestUser(unittest.TestCase):
    def test_member_creation(self):
        member = Member(1, "Alice", "standard")
        assert member.borrow_limit == 3

    def test_premium_member_limit(self):
        member = Member(1, "Alice", "premium")
        assert member.borrow_limit == 7

    def test_admin_creation(self):
        admin = Admin(1, "Admin")
        assert admin.borrow_limit == 10

    def test_borrow_book(self):
        member = Member(1, "Alice")
        assert member.borrow_book(101) is True
        assert 101 in member.borrowed_books

    def test_cannot_borrow_same_book_twice(self):
        member = Member(1, "Alice")
        member.borrow_book(101)
        assert member.borrow_book(101) is False

    def test_return_book(self):
        member = Member(1, "Alice")
        member.borrow_book(101)
        assert member.return_book(101) is True
        assert 101 not in member.borrowed_books

    def test_return_book_not_borrowed(self):
        member = Member(1, "Alice")
        assert member.return_book(999) is False

    def test_standard_member_borrow_limit(self):
        member = Member(1, "Alice", "standard")
        for i in range(3):
            member.borrow_book(i)
        assert member.can_borrow() is False

    def test_get_info_admin(self):
        admin = Admin(1, "Admin")
        info = admin.get_info()
        assert info["role"] == "admin"


class TestBorrowRecord(unittest.TestCase):
    def test_record_is_active(self):
        record = BorrowRecord(1, 101)
        assert record.is_active() is True

    def test_mark_returned(self):
        record = BorrowRecord(1, 101)
        record.mark_returned()
        assert record.is_active() is False
        assert record.return_date is not None

    def test_to_dict(self):
        record = BorrowRecord(1, 101, "2026-05-01 10:00:00")
        d = record.to_dict()
        assert d["user_id"] == 1
        assert d["book_id"] == 101
        assert d["return_date"] is None


class TestValidators(unittest.TestCase):
    def test_valid_name(self):
        assert is_valid_name("Alice") is True
        assert is_valid_name("") is False
        assert is_valid_name("A") is False

    def test_positive_int(self):
        assert is_positive_int(5) is True
        assert is_positive_int(0) is False
        assert is_positive_int(-3) is False
        assert is_positive_int("abc") is False

    def test_valid_membership(self):
        assert is_valid_membership("standard") is True
        assert is_valid_membership("premium") is True
        assert is_valid_membership("vip") is False


if __name__ == "__main__":
    unittest.main(verbosity=2)
