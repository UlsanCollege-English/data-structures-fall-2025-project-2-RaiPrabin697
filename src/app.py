#!/usr/bin/env python3
"""
Command-line interface for the Trie-based autocomplete system.

Available commands:
  load <path>        - Load (word, freq) pairs from CSV into the trie
  save <path>        - Save trie contents to CSV
  insert <word> <f>  - Insert a word with frequency
  remove <word>      - Delete a word from trie
  contains <word>    - Check if a word exists
  complete <pre> <k> - Get top-k completions for prefix
  stats              - Print stats (words, height, nodes)
  quit               - Exit program
"""

import sys
import os
from pathlib import Path
from typing import Tuple

# Include project root in path so imports work correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.trie import Trie
from src.io_utils import load_csv, save_csv


def handle_load(file_path: str) -> "Trie":
    """Create a new Trie populated with data from CSV file."""
    path = Path(file_path)
    data = load_csv(path)
    trie = Trie()
    for word, freq in data:
        trie.insert(word, freq)
    return trie


def handle_save(trie: "Trie", file_path: str) -> None:
    """Save trie data (word, freq) pairs into CSV file."""
    save_csv(Path(file_path), trie.items())


def handle_insert(trie: "Trie", word: str, freq: str) -> None:
    """Insert a word with its frequency into the trie."""
    trie.insert(word.lower(), float(freq))


def handle_remove(trie: "Trie", word: str) -> None:
    """Remove word if exists; print OK or MISS."""
    print("OK" if trie.remove(word.lower()) else "MISS")


def handle_contains(trie: "Trie", word: str) -> None:
    """Check if a word is in trie; print YES or NO."""
    print("YES" if trie.contains(word.lower()) else "NO")


def handle_complete(trie: "Trie", prefix: str, k: str) -> None:
    """Print top-k autocompletion results separated by commas."""
    k = int(k)
    completions = trie.complete(prefix.lower(), k)
    print(",".join(completions))


def handle_stats(trie: "Trie") -> None:
    """Print simple trie statistics."""
    total_words, height, nodes = trie.stats()
    print(f"words={total_words} height={height} nodes={nodes}")


def execute_command(line: str, trie: "Trie") -> Tuple[bool, "Trie"]:
    """Interpret and execute a single CLI command."""
    parts = line.strip().split()
    if not parts:
        return True, trie

    cmd = parts[0].lower()

    try:
        if cmd == "quit":
            return False, trie

        elif cmd == "load" and len(parts) == 2:
            trie = handle_load(parts[1])

        elif cmd == "save" and len(parts) == 2:
            handle_save(trie, parts[1])

        elif cmd == "insert" and len(parts) == 3:
            handle_insert(trie, parts[1], parts[2])

        elif cmd == "remove" and len(parts) == 2:
            handle_remove(trie, parts[1])

        elif cmd == "contains" and len(parts) == 2:
            handle_contains(trie, parts[1])

        elif cmd == "complete" and len(parts) == 3:
            handle_complete(trie, parts[1], parts[2])

        elif cmd == "stats":
            handle_stats(trie)

    except FileNotFoundError:
        print(f"ERROR: File not found - {parts[1]}", file=sys.stderr)
    except Exception as e:
        # Silently ignore invalid inputs or runtime errors to match spec
        pass

    return True, trie


def main():
    trie = Trie()
    for line in sys.stdin:
        keep_running, trie = execute_command(line, trie)
        if not keep_running:
            break


if __name__ == "__main__":
    main()
