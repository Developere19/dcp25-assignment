import os
import sqlite3
import pandas as pd

books_dir = "abc_books"
db_path = "tunes.db"

# -------------------------------------------------
# PART 1: DATABASE SETUP
# -------------------------------------------------

def init_db():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tunes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tune_id INTEGER,
            title TEXT,
            composer TEXT,
            meter TEXT,
            key TEXT,
            rhythm TEXT,
            book_number INTEGER,
            abc_notation TEXT
        )
    """)
    conn.commit()
    conn.close()


# -------------------------------------------------
# PART 1: ABC FILE PARSING
# -------------------------------------------------

def parse_abc_file(path, book_number):
    """Parse all tunes in one .abc file."""
    tunes = []
    tune = {}
    notation = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = [ln.strip() for ln in f.readlines()]
    except:
        with open(path, "r", encoding="latin-1") as f:
            lines = [ln.strip() for ln in f.readlines()]

    for line in lines:
        if line.startswith("X:"):
            if tune.get("title"):
                tune["abc_notation"] = "\n".join(notation)
                tune["book_number"] = book_number
                tunes.append(tune)

            tune = {}
            notation = []
            num = ''.join(ch for ch in line[2:] if ch.isdigit())
            tune["tune_id"] = int(num) if num else 0
        

        elif line.startswith("T:"):
            tune["title"] = line[2:]
        elif line.startswith("C:"):
            tune["composer"] = line[2:]
        elif line.startswith("M:"):
            tune["meter"] = line[2:]
        elif line.startswith("K:"):
            tune["key"] = line[2:]
        elif line.startswith("R:"):
            tune["rhythm"] = line[2:]
        elif line and not line.startswith("%"):
            notation.append(line)
    
    if tune.get("title"):
        tune["abc_notation"] = "\n".join(notation)
        tune["book_number"] = book_number
        tunes.append(tune)

    return tunes


def store_tune(tune):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO tunes VALUES
        (NULL, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        tune.get("tune_id", 0),
        tune.get("title", ""),
        tune.get("composer", ""),
        tune.get("meter", ""),
        tune.get("key", ""),
        tune.get("rhythm", ""),
        tune.get("book_number", 0),
        tune.get("abc_notation", "")
    ))

    conn.commit()
    conn.close()


# -------------------------------------------------
# PART 1: RECURSIVE DIRECTORY TRAVERSAL
# -------------------------------------------------

