from flask import Flask, session
import mysql.connector # <--- IMPOR BARU
from datetime import datetime, timedelta
# ... (impor lain)

# Initialize app
app = Flask(__name__)
app.secret_key = "any_secret_key" 

# --- KONSTANTA HOST DATABASE MYSQL ---
MYSQL_HOST = "nissakhra.mysql.pythonanywhere-services.com"
MYSQL_USER = "nissakhra"
MYSQL_PASSWORD = "username!"
db_user = "nissakhra$users"
db_soal = "nissakhra$soal"

cities = [
            "jakarta", "bandung", "surabaya",
            "medan", "makassar", "yogyakarta",
            "bali", "palembang", "semarang",
            "malang", "padang", "pekanbaru",
            "batam", "manado", "banjarmasin"
        ]

# --- FUNGSI UTAMA KONEKSI MYSQL ---
def get_db_connection(database):
    """Mengembalikan objek koneksi ke database MySQL."""
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=database,
            charset='utf8mb4'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error Koneksi MySQL: {err}")
        # Di lingkungan produksi, Anda mungkin ingin me-raise exception 
        # atau melakukan logging yang lebih baik.
        return None

# --- FUNGSI INIT DB BARU UNTUK MYSQL ---

def init_db():
    conn = get_db_connection(db_user)
    if conn is None:
        return # Gagal koneksi, keluar

    cursor = conn.cursor()

    # Membuat tabel users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            score INT DEFAULT 0
        ) ENGINE=InnoDB
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

init_db()


def init_soal_db():
    """Membuat tabel questions untuk soal kuis."""
    conn = get_db_connection(db_soal)
    if conn is None:
        return # Gagal koneksi, keluar

    cursor = conn.cursor()

    # Membuat tabel questions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            question TEXT NOT NULL,
            option_a VARCHAR(500),
            option_b VARCHAR(500),
            option_c VARCHAR(500),
            option_d VARCHAR(500),
            correct_answer VARCHAR(1) NOT NULL
        ) ENGINE=InnoDB
    """)

    conn.commit()
    cursor.close()
    conn.close()

init_soal_db()

# ... (lanjutan code Flask Anda)