import os
import sqlite3
import pandas as pd

books_dir = "abc_books"
db_path = "tunes.db"


# PART 1: DATABASE SETUP


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



# PART 1: ABC FILE PARSING


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



# PART 1: RECURSIVE DIRECTORY TRAVERSAL


def process_all_books():
    """Recursively scan abc_books/, parse abc files, insert into DB."""
    print("\nScanning and processing ABC files...\n")
    total = 0

    for root, dirs, files in os.walk(books_dir):
        folder = os.path.basename(root)

        if folder.isdigit():
            book_num = int(folder)
            print(f" Book {book_num}")

            for f in files:
                if f.endswith(".abc"):
                    fp = os.path.join(root, f)
                    tunes = parse_abc_file(fp, book_num)
                    for t in tunes:
                        store_tune(t)

                    total += len(tunes)
                    print(f"   {f}: {len(tunes)} tune(s)")

    print("\nTotal tunes stored:", total)


# PART 2: PANDAS DATA LOADING + ANALYSIS
def load_data():
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM tunes", conn)
    conn.close()
    return df


def get_tunes_by_book(df, book_number):
    return df[df["book_number"] == book_number]


def get_tunes_by_type(df, tune_type):
    return df[df["rhythm"].str.contains(tune_type, case=False, na=False)]


def search_tunes(df, term):
    return df[df["title"].str.contains(term, case=False, na=False)]


def get_tunes_by_composer(df, composer):
    return df[df["composer"].str.contains(composer, case=False, na=False)]

# PART 3: BETTER INTERACTIVE MENU UI


def print_header():
    print("\n" + "=" * 60)
    print("                   ABC TUNE DATABASE SYSTEM")
    print("=" * 60)

def print_menu():
    print("\n" + "-" * 60)
    print("                     MAIN MENU")
    print("-" * 60)
    print(" [1]  Search tunes by title")
    print(" [2]  Get tunes by book number")
    print(" [3]  Get tunes by rhythm type")
    print(" [4]  Load ABC files into database")
    print(" [5]  View dataframe summary")
    print(" [6]  Exit")
    print("-" * 60)

def print_box(title):
    print("\n" + "-" * 60)
    print(f" {title}")
    print("-" * 60)
    
def run_menu():
    init_db()
    print_header()

    try:
        df = load_data()
        print(f" Loaded {len(df)} tunes from the database.")
    except:
        df = pd.DataFrame()
        print(" No existing data found. Use option 4 to load ABC files.")
    
    while True:
        print_menu()
        choice = input(" Enter choice (1-6): ").strip()

        # Option 1
        if choice == "1":
            print_box("Search Tunes by Title")
            term = input(" Enter search term: ")
            result = search_tunes(df, term)
            print("\n" result)