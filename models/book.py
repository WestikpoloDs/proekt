class Book:
    def __init__(self, book_id: int, title: str, author: str, available: bool = True):
        self._book_id = book_id
        self._title = title
        self._author = author
        self._available = available

    @property
    def book_id(self) -> int:
        return self._book_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def author(self) -> str:
        return self._author

    @property
    def available(self) -> bool:
        return self._available

    @available.setter
    def available(self, value: bool):
        self._available = value

    def to_dict(self) -> dict:
        return {
            "id": self._book_id,
            "title": self._title,
            "author": self._author,
            "available": self._available,
        }

    def __repr__(self) -> str:
        status = "available" if self._available else "borrowed"
        return f"Book(id={self._book_id}, title='{self._title}', author='{self._author}', {status})"
