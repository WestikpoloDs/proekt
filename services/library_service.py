from models.transaction import BorrowRecord
from services.book_service import BookService
from services.user_service import UserService
from utils.file_handler import load_json, save_json

HISTORY_FILE = "data/history.json"


class LibraryService:
    def __init__(self):
        self.books = BookService()
        self.users = UserService()
        self._history: list[BorrowRecord] = []
        self._load_history()

    def _load_history(self):
        raw = load_json(HISTORY_FILE)
        for item in raw:
            record = BorrowRecord(item["user_id"], item["book_id"], item["borrow_date"])
            if item.get("return_date"):
                record.mark_returned()
                record._return_date = item["return_date"]
            self._history.append(record)

    def _save_history(self):
        save_json(HISTORY_FILE, [r.to_dict() for r in self._history])

    def borrow_book(self, user_id: int, book_id: int) -> tuple[bool, str]:
        user = self.users.get_user(user_id)
        if user is None:
            return False, "User not found."

        book = self.books.get_book(book_id)
        if book is None:
            return False, "Book not found."

        if not book.available:
            return False, f"'{book.title}' is not available."

        if not user.can_borrow():
            return False, f"{user.name} has reached their borrow limit."

        success = user.borrow_book(book_id)
        if not success:
            return False, f"{user.name} already has this book."

        self.books.set_availability(book_id, False)
        self.users.save()

        record = BorrowRecord(user_id, book_id)
        self._history.append(record)
        self._save_history()

        return True, f"'{book.title}' borrowed by {user.name}."

    def return_book(self, user_id: int, book_id: int) -> tuple[bool, str]:
        user = self.users.get_user(user_id)
        if user is None:
            return False, "User not found."

        book = self.books.get_book(book_id)
        if book is None:
            return False, "Book not found."

        success = user.return_book(book_id)
        if not success:
            return False, f"{user.name} does not have book '{book.title}'."

        self.books.set_availability(book_id, True)
        self.users.save()

        for record in reversed(self._history):
            if record.user_id == user_id and record.book_id == book_id and record.is_active():
                record.mark_returned()
                break

        self._save_history()
        return True, f"'{book.title}' returned by {user.name}."

    def get_user_history(self, user_id: int) -> list[BorrowRecord]:
        return [r for r in self._history if r.user_id == user_id]

    def get_active_borrows(self) -> list[BorrowRecord]:
        return [r for r in self._history if r.is_active()]

    def get_full_history(self) -> list[BorrowRecord]:
        return list(self._history)

    def statistics(self) -> dict:
        total_books = len(self.books.get_all_books())
        available = len(self.books.get_available_books())
        borrowed = len(self.books.get_borrowed_books())
        total_users = len(self.users.get_all_users())
        active_borrows = len(self.get_active_borrows())
        total_transactions = len(self._history)

        borrow_counts: dict[int, int] = {}
        for record in self._history:
            borrow_counts[record.book_id] = borrow_counts.get(record.book_id, 0) + 1

        most_borrowed_id = max(borrow_counts, key=lambda x: borrow_counts[x], default=None)
        most_borrowed = None
        if most_borrowed_id is not None:
            book = self.books.get_book(most_borrowed_id)
            most_borrowed = f"{book.title} ({borrow_counts[most_borrowed_id]} times)" if book else None

        return {
            "total_books": total_books,
            "available_books": available,
            "borrowed_books": borrowed,
            "total_users": total_users,
            "active_borrows": active_borrows,
            "total_transactions": total_transactions,
            "most_borrowed": most_borrowed,
        }
