"""
Utility functions for reading and writing (word, score) data in CSV format.
Each row should contain: word, score
"""

import csv


def load_csv(file_path):
    """
    Reads a two-column CSV file and returns a list of (word, score) tuples.
    The 'score' is converted to float, or defaults to 0.0 if not valid.
    """
    words = []
    try:
        with open(file_path, "r", encoding="utf-8", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 0:
                    continue

                word = row[0].strip().lower()
                try:
                    score = float(row[1]) if len(row) > 1 else 0.0
                except ValueError:
                    score = 0.0

                words.append((word, score))
    except FileNotFoundError:
        print(f"ERROR: Missing file at {file_path}")
        return []
    except Exception as err:
        print(f"ERROR: Failed to load {file_path}: {err}")
        return []

    return words


def save_csv(file_path, data):
    """
    Writes a list of (word, score) pairs to the given CSV file path.
    The file will be overwritten if it already exists.
    """
    try:
        with open(file_path, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            for word, score in data:
                writer.writerow([word, score])
    except Exception as err:
        print(f"ERROR: Could not save file {file_path}: {err}")
