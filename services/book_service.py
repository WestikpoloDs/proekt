from models.book import Book
from utils.file_handler import load_json, save_json

BOOKS_FILE = "data/books.json"


class BookService:
    def __init__(self):
        self._books: dict[int, Book] = {}
        self._load()

    def _load(self):
        raw = load_json(BOOKS_FILE)
        for item in raw:
            book = Book(item["id"], item["title"], item["author"], item["available"])
            self._books[book.book_id] = book

    def save(self):
        save_json(BOOKS_FILE, [b.to_dict() for b in self._books.values()])

    def add_book(self, book_id: int, title: str, author: str) -> tuple[bool, str]:
        if book_id in self._books:
            return False, f"Book with id {book_id} already exists."
        self._books[book_id] = Book(book_id, title, author)
        self.save()
        return True, f"Book '{title}' added."

    def remove_book(self, book_id: int) -> tuple[bool, str]:
        if book_id not in self._books:
            return False, "Book not found."
        if not self._books[book_id].available:
            return False, "Cannot remove a borrowed book."
        del self._books[book_id]
        self.save()
        return True, "Book removed."

    def get_book(self, book_id: int) -> Book | None:
        return self._books.get(book_id)

    def get_all_books(self) -> list[Book]:
        return list(self._books.values())

    def get_available_books(self) -> list[Book]:
        return [b for b in self._books.values() if b.available]

    def get_borrowed_books(self) -> list[Book]:
        return [b for b in self._books.values() if not b.available]

    def search_books(self, query: str) -> list[Book]:
        query = query.lower()
        return [
            b for b in self._books.values()
            if query in b.title.lower() or query in b.author.lower()
        ]

    def set_availability(self, book_id: int, available: bool) -> bool:
        book = self._books.get(book_id)
        if book is None:
            return False
        book.available = available
        self.save()
        return True

    def iter_books(self):
        yield from self._books.values()

    def next_id(self) -> int:
        return max(self._books.keys(), default=0) + 1
