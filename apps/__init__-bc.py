from flask import Flask, session
import sqlite3

# Initialize app
app = Flask(__name__)
app.secret_key = "any_secret_key" 

# Define constants
DB_USER = "users.db"
DB_SOAL = "soal.db"
cities = [
            "jakarta", "bandung", "surabaya",
            "medan", "makassar", "yogyakarta",
            "bali", "palembang", "semarang",
            "malang", "padang", "pekanbaru",
            "batam", "manado", "banjarmasin"
        ]

# Context processor
@app.context_processor
def inject_user():
    return dict(session=session)

def init_db():
    conn = sqlite3.connect(DB_USER)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT,
            score INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()
init_db()

def init_soal_db():
    """Hanya untuk memastikan tabel questions ada, data diisi via input_soal.py"""
    conn = sqlite3.connect(DB_SOAL)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            option_a TEXT,
            option_b TEXT,
            option_c TEXT,
            option_d TEXT,
            correct_answer TEXT
        )
    """)
    conn.commit()
    conn.close()
init_soal_db()