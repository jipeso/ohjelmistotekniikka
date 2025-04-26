import json
from pathlib import Path


def ensure_file_exists(file_path):
    Path(file_path).touch()


def write_json_file(file_path, data):
    ensure_file_exists(file_path)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def read_json_file(file_path):
    ensure_file_exists(file_path)
    with open(file_path, encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []
