import os
import sqlite3
import pandas as pd
import re
from typing import List, Dict

class ABCparser:

    def __init__(self, books_dir: str = "abc_books", db_path: str = "tunes.db"):
        self.books_dir = books_dir
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tunes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tune_id INTEGER, title TEXT, composer TEXT, meter TEXT,
                key TEXT, rhythm TEXT, book_number INTEGER, abc_notation TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def process_books(self) -> int:
                total_tunes = 0
                print(" Processing ABC Files...")
                print("─" * 40)
                
                for item in os.listdir(self.books_dir):
                    item_path = os.path.join(self.books_dir, item)
                    if os.path.isdir(item_path) and item.isdigit():
                        book_num = int(item)
                        tunes = self._process_book(item_path, book_num)
                        total_tunes += tunes
                        print(f" Book {book_num}: {tunes:2d} tunes")
                
                print("─" * 40)
                print(f" Total: {total_tunes} tunes stored")
                return total_tunes
        

    def _process_book(self, dir_path: str, book_num: int) -> int:
        tunes_count = 0
        for file in os.listdir(dir_path):
            if file.endswith('.abc'):
                file_path = os.path.join(dir_path, file)
                tunes = self._parse_file(file_path, book_num)
                tunes_count += len(tunes)
                for tune in tunes:
                    self._store_tune(tune)
        return tunes_count
        
        