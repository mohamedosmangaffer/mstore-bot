import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "../../orders.db")

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                user_id INTEGER,
                name TEXT,
                service TEXT,
                time TEXT,
                attachment TEXT DEFAULT NULL,
                order_id TEXT DEFAULT NULL,
                status TEXT DEFAULT 'pending'
            )
        """)
