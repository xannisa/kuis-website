import sqlite3

DB_NAME = "soal.db"   # sesuaikan dengan nama database kamu

questions = [
    (
        "Apakah kepanjangan yang paling tepat dari akronim NLP?",
        "Neuro-Linguistik Psikologi",
        "Neurologi-Lingual Pemikiran",
        "Neuro-Linguistic Programming",
        "Nature-Logic Psychology",
        "C"
    ),
    (
        "Siapakah dua tokoh yang diakui sebagai pendiri awal dan pengembang utama NLP?",
        "Sigmund Freud dan Carl Jung",
        "Ivan Pavlov dan B.F. Skinner",
        "Virginia Satir dan Milton H. Erickson",
        "Richard Bandler dan John Grinder",
        "D"
    ),
    (
        "Manakah di antara pernyataan berikut yang merupakan salah satu 'presuposisi' dasar dalam NLP?",
        "Peta adalah wilayah",
        "Komunikasi yang efektif hanya terjadi jika kata-kata 100% akurat",
        "Tidak ada kegagalan, hanya umpan balik",
        "Orang-orang termotivasi hanya oleh uang dan kekuasaan",
        "C"
    ),
    (
        "Dalam konteks Representational Systems, apa yang diwakili oleh huruf 'K' dalam VAKOG?",
        "Kognitif (Pemikiran)",
        "Kinestetik (Perasaan/Sentuhan)",
        "Konteks (Lingkungan)",
        "Kreatif (Imajinasi)",
        "B"
    ),
    (
        "Teknik NLP yang melibatkan pengaitan respons internal tertentu dengan pemicu eksternal disebut...",
        "Reframing",
        "Pattern Interrupt",
        "Anchoring (Penjangkaran)",
        "Swish Pattern",
        "C"
    ),
    (
        "Tujuan utama dari penggunaan Meta Model dalam NLP adalah untuk...",
        "Mengubah makna suatu peristiwa",
        "Menggunakan pola bahasa yang kabur",
        "Mengidentifikasi dan mengklarifikasi distorsi, generalisasi, dan penghapusan",
        "Menciptakan kondisi emosional puncak",
        "C"
    ),
    (
        "Dalam Model Komunikasi NLP, ada tiga proses filter utama: ...",
        "VAKOG, Submodalitas, dan Reframing",
        "Persepsi, Emosi, dan Keputusan",
        "Metamodel, Milton Model, dan Strategi",
        "Penghapusan, Distorsi, dan Generalisasi",
        "D"
    ),
    (
        "Dalam NLP, 'submodalitas' mengacu pada...",
        "Cara orang beralih antara sistem representasional",
        "Strategi di balik semua keputusan",
        "Detail-detail indrawi yang membentuk pengalaman internal",
        "Nilai dan keyakinan inti",
        "C"
    ),
    (
        "Teknik 'Swish Pattern' dalam NLP bertujuan untuk...",
        "Menetapkan jangkar kinestetik",
        "Mengubah keyakinan yang membatasi",
        "Mengubah pola perilaku yang tidak diinginkan dengan mengganti gambaran mental",
        "Menciptakan bahasa yang kabur untuk trance",
        "C"
    ),
    (
        "Milton Model dalam NLP dinamai dari siapa dan paling sering digunakan untuk apa?",
        "Virginia Satir; untuk memecahkan konflik keluarga",
        "Gregory Bateson; untuk menganalisis sistem sosial",
        "Milton H. Erickson; untuk menciptakan ambiguitas dan trance",
        "Alfred Korzybski; untuk mengoreksi bias dalam bahasa",
        "C"
    ),
]

def seed_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Buat tabel jika belum ada
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

    # Masukkan data
    cursor.executemany("""
        INSERT INTO questions
        (question, option_a, option_b, option_c, option_d, correct_answer)
        VALUES (?, ?, ?, ?, ?, ?)
    """, questions)

    conn.commit()
    conn.close()

    print("✔ Semua soal berhasil dimasukkan ke database!")

if __name__ == "__main__":
    seed_data()
