class User:
    def __init__(self, user_id: int, name: str):
        self._user_id = user_id
        self._name = name
        self._borrowed_books: list[int] = []

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def borrowed_books(self) -> list[int]:
        return self._borrowed_books

    @borrowed_books.setter
    def borrowed_books(self, books: list[int]):
        self._borrowed_books = books

    def borrow_book(self, book_id: int) -> bool:
        if book_id in self._borrowed_books:
            return False
        self._borrowed_books.append(book_id)
        return True

    def return_book(self, book_id: int) -> bool:
        if book_id not in self._borrowed_books:
            return False
        self._borrowed_books.remove(book_id)
        return True

    def get_info(self) -> dict:
        return {
            "user_id": self._user_id,
            "name": self._name,
            "borrowed_books": self._borrowed_books,
        }

    def __repr__(self) -> str:
        return f"User(id={self._user_id}, name={self._name})"


class Member(User):
    def __init__(self, user_id: int, name: str, membership_type: str = "standard"):
        super().__init__(user_id, name)
        self._membership_type = membership_type
        self._borrow_limit = 3 if membership_type == "standard" else 7

    @property
    def membership_type(self) -> str:
        return self._membership_type

    @property
    def borrow_limit(self) -> int:
        return self._borrow_limit

    def can_borrow(self) -> bool:
        return len(self._borrowed_books) < self._borrow_limit

    def get_info(self) -> dict:
        info = super().get_info()
        info["role"] = "member"
        info["membership_type"] = self._membership_type
        info["borrow_limit"] = self._borrow_limit
        return info

    def __repr__(self) -> str:
        return f"Member(id={self._user_id}, name={self._name}, type={self._membership_type})"


class Admin(User):
    def __init__(self, user_id: int, name: str):
        super().__init__(user_id, name)
        self._borrow_limit = 10

    @property
    def borrow_limit(self) -> int:
        return self._borrow_limit

    def can_borrow(self) -> bool:
        return len(self._borrowed_books) < self._borrow_limit

    def get_info(self) -> dict:
        info = super().get_info()
        info["role"] = "admin"
        info["borrow_limit"] = self._borrow_limit
        return info

    def __repr__(self) -> str:
        return f"Admin(id={self._user_id}, name={self._name})"
