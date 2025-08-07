
import sqlite3
import os
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

base_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_path, "sql.db")


def sql_engine():
    return create_engine(
        f"sqlite:///{file_path}",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool  # good for single-threaded apps
    )


def initialize_db():
    """Check if database needs to be initialized."""
    if not os.path.exists(file_path):
        return True

    try:
        conn = sqlite3.connect(file_path)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM Patients")
        cur.fetchone()
        return False  # already initialized
    except sqlite3.OperationalError:
        return True
    finally:
        conn.close()


def create_db():
    """Create and initialize the SQLite database from SQL schema."""
    if not initialize_db():
        print("✅ DB already initialized.")
        return

    print("🚀 Initializing DB...")

    with sqlite3.connect(file_path) as conn:
        with open(os.path.join(os.path.dirname(__file__), "schema.sql"), 'r') as file:
            schema = file.read()
            conn.executescript(schema)

    print("✅ SQLite database created with sample data.")
