from pathlib import Path


def ensure_file_exists(file_path):
    Path(file_path).touch()


def write_file_lines(file_path, rows):
    ensure_file_exists(file_path)
    with open(file_path, "w", encoding="utf-8") as file:
        for row in rows:
            file.write(";".join(map(str, row)) + "\n")


def read_file_lines(file_path):
    ensure_file_exists(file_path)
    with open(file_path, encoding="utf-8") as file:
        return [line.strip().split(";") for line in file]
