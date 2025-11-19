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