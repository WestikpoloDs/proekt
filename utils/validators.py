import re


def is_valid_name(name: str) -> bool:
    return bool(re.match(r"^[A-Za-z\s'-]{2,60}$", name.strip()))


def is_positive_int(value) -> bool:
    try:
        return int(value) > 0
    except (ValueError, TypeError):
        return False


def is_valid_membership(membership: str) -> bool:
    return membership in {"standard", "premium"}


def is_valid_role(role: str) -> bool:
    return role in {"member", "admin"}