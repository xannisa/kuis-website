from flask import Flask, session
import mysql.connector # <--- IMPOR BARU
from datetime import datetime, timedelta
import json 
import os
from mysql.connector import Error
import sys
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

# --- KONSTANTA FILE DATA ---
question_file = "questions.json" 

def load_questions_from_json():
    """Memuat soal dari berkas JSON dan mengkonversi ke format tuple untuk MySQL."""
    if not os.path.exists(question_file):
        print(f"❌ ERROR: Berkas data {question_file} tidak ditemukan!")
        sys.exit(1)

    with open(question_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # Konversi data JSON ke format tuple (question, A, B, C, D, answer)
    questions_for_db = []
    for q_obj in json_data:
        q_tuple = (
            q_obj["question"],
            q_obj["options"]["A"],
            q_obj["options"]["B"],
            q_obj["options"]["C"],
            q_obj["options"]["D"],
            q_obj["answer"]
        )
        questions_for_db.append(q_tuple)
        
    return questions_for_db


def seed_data_mysql():
    questions_to_seed = load_questions_from_json()
    if not questions_to_seed:
        print("Tidak ada soal yang dimuat untuk seeding.")
        return

    print("Mencoba menghubungkan ke MySQL...")
    conn = get_db_connection(db_soal)
    if conn is None:
        return

    cursor = conn.cursor()
    insert_query = """
        INSERT INTO questions
        (question, option_a, option_b, option_c, option_d, correct_answer)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    try:
        # Masukkan data
        cursor.executemany(insert_query, questions_to_seed)
        
        conn.commit()
        print(f"✔ Berhasil memasukkan {cursor.rowcount} soal kuis dari {question_file} ke tabel 'questions'.")

    except Error as err:
        print(f"❌ Error saat memasukkan data: {err}")
        conn.rollback()
        
    finally:
        cursor.close()
        conn.close()

load_questions_from_json()
seed_data_mysql()