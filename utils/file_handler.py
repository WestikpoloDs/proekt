import json
import os


def load_json(filepath: str) -> list | dict:
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filepath: str, data: list | dict) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def append_to_json(filepath: str, new_entry: dict) -> None:
    data = load_json(filepath)
    if not isinstance(data, list):
        data = []
    data.append(new_entry)
    save_json(filepath, data)