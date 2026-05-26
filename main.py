import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.library_service import LibraryService
from utils.validators import is_valid_name, is_positive_int, is_valid_membership, is_valid_role


def print_separator():
    print("-" * 50)


def print_menu():
    print("\n Library Management System")
    print("1.  List all books")
    print("2.  List available books")
    print("3.  List borrowed books")
    print("4.  Search books")
    print("5.  Add book")
    print("6.  Remove book")
    print("7.  List all users")
    print("8.  Add user")
    print("9.  Remove user")
    print("10. Borrow book")
    print("11. Return book")
    print("12. View user history")
    print("13. View all active borrows")
    print("14. Statistics")
    print("0.  Exit")
    print_separator()


def get_int_input(prompt: str) -> int | None:
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None


def handle_list_all_books(lib: LibraryService):
    books = lib.books.get_all_books()
    if not books:
        print("No books found.")
        return
    print_separator()
    for book in books:
        status = "Available" if book.available else "Borrowed"
        print(f"[{book.book_id}] {book.title} — {book.author} [{status}]")


def handle_available_books(lib: LibraryService):
    books = lib.books.get_available_books()
    if not books:
        print("No available books.")
        return
    print_separator()
    for book in books:
        print(f"[{book.book_id}] {book.title} — {book.author}")


def handle_borrowed_books(lib: LibraryService):
    books = lib.books.get_borrowed_books()
    if not books:
        print("No borrowed books.")
        return
    print_separator()
    for book in books:
        print(f"[{book.book_id}] {book.title} — {book.author}")


def handle_search_books(lib: LibraryService):
    query = input("Search query: ").strip()
    results = lib.books.search_books(query)
    if not results:
        print("No books found.")
        return
    for book in results:
        status = "Available" if book.available else "Borrowed"
        print(f"[{book.book_id}] {book.title} — {book.author} [{status}]")


def handle_add_book(lib: LibraryService):
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    if not title or not author:
        print("Title and author cannot be empty.")
        return
    book_id = lib.books.next_id()
    ok, msg = lib.books.add_book(book_id, title, author)
    print(msg)


def handle_remove_book(lib: LibraryService):
    book_id = get_int_input("Book ID: ")
    if book_id is None:
        return
    ok, msg = lib.books.remove_book(book_id)
    print(msg)


def handle_list_users(lib: LibraryService):
    users = lib.users.get_all_users()
    if not users:
        print("No users found.")
        return
    print_separator()
    for user in users:
        info = user.get_info()
        role = info.get("role", "member")
        borrowed = info.get("borrowed_books", [])
        print(f"[{user.user_id}] {user.name} ({role}) — borrowed: {borrowed}")


def handle_add_user(lib: LibraryService):
    name = input("Name: ").strip()
    if not is_valid_name(name):
        print("Invalid name.")
        return
    role = input("Role (member/admin): ").strip().lower()
    if not is_valid_role(role):
        print("Invalid role.")
        return
    membership = "standard"
    if role == "member":
        membership = input("Membership (standard/premium): ").strip().lower()
        if not is_valid_membership(membership):
            print("Invalid membership type.")
            return
    user_id = lib.users.next_id()
    ok, msg = lib.users.add_user(user_id, name, role, membership)
    print(msg)


def handle_remove_user(lib: LibraryService):
    user_id = get_int_input("User ID: ")
    if user_id is None:
        return
    ok, msg = lib.users.remove_user(user_id)
    print(msg)


def handle_borrow(lib: LibraryService):
    user_id = get_int_input("User ID: ")
    if user_id is None:
        return
    book_id = get_int_input("Book ID: ")
    if book_id is None:
        return
    ok, msg = lib.borrow_book(user_id, book_id)
    print(msg)


def handle_return(lib: LibraryService):
    user_id = get_int_input("User ID: ")
    if user_id is None:
        return
    book_id = get_int_input("Book ID: ")
    if book_id is None:
        return
    ok, msg = lib.return_book(user_id, book_id)
    print(msg)


def handle_user_history(lib: LibraryService):
    user_id = get_int_input("User ID: ")
    if user_id is None:
        return
    user = lib.users.get_user(user_id)
    if user is None:
        print("User not found.")
        return
    history = lib.get_user_history(user_id)
    if not history:
        print(f"No history for {user.name}.")
        return
    print(f"\nHistory for {user.name}:")
    print_separator()
    for record in history:
        book = lib.books.get_book(record.book_id)
        title = book.title if book else f"Book #{record.book_id}"
        status = "Active" if record.is_active() else f"Returned: {record.return_date}"
        print(f"  '{title}' — Borrowed: {record.borrow_date} | {status}")


def handle_active_borrows(lib: LibraryService):
    active = lib.get_active_borrows()
    if not active:
        print("No active borrows.")
        return
    print_separator()
    for record in active:
        user = lib.users.get_user(record.user_id)
        book = lib.books.get_book(record.book_id)
        user_name = user.name if user else f"User #{record.user_id}"
        book_title = book.title if book else f"Book #{record.book_id}"
        print(f"  {user_name} → '{book_title}' (since {record.borrow_date})")


def handle_statistics(lib: LibraryService):
    stats = lib.statistics()
    print_separator()
    print(f"Total books       : {stats['total_books']}")
    print(f"Available books   : {stats['available_books']}")
    print(f"Borrowed books    : {stats['borrowed_books']}")
    print(f"Total users       : {stats['total_users']}")
    print(f"Active borrows    : {stats['active_borrows']}")
    print(f"Total transactions: {stats['total_transactions']}")
    if stats["most_borrowed"]:
        print(f"Most borrowed     : {stats['most_borrowed']}")


HANDLERS = {
    1: handle_list_all_books,
    2: handle_available_books,
    3: handle_borrowed_books,
    4: handle_search_books,
    5: handle_add_book,
    6: handle_remove_book,
    7: handle_list_users,
    8: handle_add_user,
    9: handle_remove_user,
    10: handle_borrow,
    11: handle_return,
    12: handle_user_history,
    13: handle_active_borrows,
    14: handle_statistics,
}


def run():
    lib = LibraryService()
    while True:
        print_menu()
        choice = get_int_input("Choose an option: ")
        if choice is None:
            continue
        if choice == 0:
            print("Goodbye!")
            break
        handler = HANDLERS.get(choice)
        if handler:
            handler(lib)
        else:
            print("Invalid option.")


if __name__ == "__main__":
    run()
