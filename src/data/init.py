import os
from pathlib import Path
from sqlite3 import Connection, Cursor, IntegrityError, connect

conn: Connection | None = None
curs: Cursor | None = None


def get_db(name: str | None = None, reset: bool = False):
    """Подключение к файлу SQLite"""
    global conn, curs
    if conn:
        if not reset:
            return
        conn = None
    if not name:
        top_dir = Path(__file__).resolve().parent.parent.parent # repo top
        db_name = "cryptid.db"
        db_path = str(top_dir / db_name)
        name = os.getenv("CRYPTID_SQLITE_DB", db_path)
    conn = connect(name, check_same_thread=False)
    curs = conn.cursor()


get_db()
