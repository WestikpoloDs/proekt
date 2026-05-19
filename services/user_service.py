from models.user import User, Member, Admin
from utils.file_handler import load_json, save_json

USERS_FILE = "data/users.json"


def _build_user(item: dict) -> User:
    role = item.get("role", "member")
    user_id = item["user_id"]
    name = item["name"]
    borrowed = item.get("borrowed_books", [])

    if role == "admin":
        user = Admin(user_id, name)
    else:
        membership = item.get("membership_type", "standard")
        user = Member(user_id, name, membership)

    user.borrowed_books = borrowed
    return user


class UserService:
    def __init__(self):
        self._users: dict[int, User] = {}
        self._load()

    def _load(self):
        raw = load_json(USERS_FILE)
        for item in raw:
            user = _build_user(item)
            self._users[user.user_id] = user

    def save(self):
        save_json(USERS_FILE, [u.get_info() for u in self._users.values()])

    def add_user(self, user_id: int, name: str, role: str = "member", membership: str = "standard") -> tuple[bool, str]:
        if user_id in self._users:
            return False, f"User with id {user_id} already exists."
        if role == "admin":
            user = Admin(user_id, name)
        else:
            user = Member(user_id, name, membership)
        self._users[user_id] = user
        self.save()
        return True, f"User '{name}' added as {role}."

    def remove_user(self, user_id: int) -> tuple[bool, str]:
        user = self._users.get(user_id)
        if user is None:
            return False, "User not found."
        if user.borrowed_books:
            return False, "User has borrowed books. Return them first."
        del self._users[user_id]
        self.save()
        return True, "User removed."

    def get_user(self, user_id: int) -> User | None:
        return self._users.get(user_id)

    def get_all_users(self) -> list[User]:
        return list(self._users.values())

    def next_id(self) -> int:
        return max(self._users.keys(), default=0) + 1
