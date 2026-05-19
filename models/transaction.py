from datetime import datetime


class BorrowRecord:
    def __init__(self, user_id: int, book_id: int, borrow_date: str = None):
        self._user_id = user_id
        self._book_id = book_id
        self._borrow_date = borrow_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._return_date: str | None = None

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def book_id(self) -> int:
        return self._book_id

    @property
    def borrow_date(self) -> str:
        return self._borrow_date

    @property
    def return_date(self) -> str | None:
        return self._return_date

    def mark_returned(self):
        self._return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def is_active(self) -> bool:
        return self._return_date is None

    def to_dict(self) -> dict:
        return {
            "user_id": self._user_id,
            "book_id": self._book_id,
            "borrow_date": self._borrow_date,
            "return_date": self._return_date,
        }

    def __repr__(self) -> str:
        status = "active" if self.is_active() else f"returned {self._return_date}"
        return f"BorrowRecord(user={self._user_id}, book={self._book_id}, {status})"
