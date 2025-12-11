from flask import request, session, flash, redirect, url_for, render_template
from .__init__ import app, db_user, db_soal, get_db_connection
import sqlite3

# --- RUTE KUIS (FLOW PER SOAL) ---

@app.route("/kuis_start")
def kuis_start():
    """Menginisialisasi state kuis: mengambil 5 soal acak dan reset skor."""
    if "user_id" not in session:
        flash("Anda harus login untuk memulai kuis.")
        return redirect(url_for("login"))

    conn = get_db_connection(db_soal)
    cursor = conn.cursor()

    # Ambil 5 ID soal secara acak (sesuaikan dengan jumlah soal di input_soal.py)
    cursor.execute("SELECT id FROM questions ORDER BY RANDOM() LIMIT 5") 
    question_ids = [row[0] for row in cursor.fetchall()]
    conn.close()

    # Cek jika tidak ada soal yang diambil (database kosong)
    if not question_ids:
        flash("Database soal kuis kosong. Mohon hubungi admin.", "error")
        return redirect(url_for("home"))

    # Simpan state kuis di session
    session["quiz_questions"] = question_ids
    session["quiz_index"] = 0
    session["quiz_score"] = 0

    return redirect(url_for("kuis"))


@app.route("/kuis", methods=["GET", "POST"])
def kuis():
    if "user_id" not in session:
        return redirect(url_for("login"))

    questions = session.get("quiz_questions")
    index = session.get("quiz_index")

    # Guard: Cek apakah kuis sudah diinisialisasi
    if questions is None or index is None:
        return redirect(url_for("kuis_start"))

    # --- LOGIKA POST (MEMPROSES JAWABAN SOAL SEBELUMNYA) ---
    if request.method == "POST":
        # Ambil QID dan jawaban dari form
        qid_from_form = request.form.get("qid")
        answer = request.form.get("answer")

        # Cek apakah jawaban sudah dipilih
        if not answer:
            flash("Anda harus memilih jawaban sebelum melanjutkan!", "warning")
            return redirect(url_for("kuis"))
        
        # Cek jawaban dengan DB
        conn = sqlite3.connect("soal.db")
        cursor = conn.cursor()
        cursor.execute("SELECT correct_answer FROM questions WHERE id = ?", (qid_from_form,))
        correct_answer = cursor.fetchone()[0]
        conn.close()

        # Update skor jika jawaban benar
        if answer == correct_answer:
            session["quiz_score"] = session["quiz_score"] + 1
            # flash("Jawaban Anda Benar!", "success") <--- DIHAPUS
        else:
            # flash(f"Jawaban Anda Salah. Jawaban yang benar adalah {correct_answer}.", "error") <--- DIHAPUS
            pass # Lanjutkan tanpa flash

        # Lanjut ke soal berikutnya
        session["quiz_index"] = index + 1
        index = session["quiz_index"] # Perbarui index lokal

        # Cek apakah kuis selesai setelah inkremen
        if index >= len(questions):
            return redirect(url_for("kuis_result"))

        # Redirect ke GET untuk menampilkan soal berikutnya
        return redirect(url_for("kuis"))

    # --- LOGIKA GET (MENAMPILKAN SOAL SAAT INI) ---
    
    # Cek apakah kuis sudah selesai
    if index >= len(questions):
        return redirect(url_for("kuis_result"))

    current_qid = questions[index]

    conn = sqlite3.connect("soal.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, question, option_a, option_b, option_c, option_d FROM questions WHERE id = ?", (current_qid,))
    q_data = cursor.fetchone()
    conn.close()

    question = {
        "id": q_data[0],
        "question": q_data[1],
        "A": q_data[2],
        "B": q_data[3],
        "C": q_data[4],
        "D": q_data[5],
    }
    
    # Teks tombol akan berubah menjadi "Selesai" jika ini adalah soal terakhir
    is_last_question = (index + 1) == len(questions)

    return render_template("kuis.html",
                           q=question,
                           index=index + 1,
                           total=len(questions),
                           is_last_question=is_last_question)


@app.route("/kuis_result")
def kuis_result():
    """Menampilkan hasil, menyimpan skor ke DB user, dan membersihkan sesi kuis."""
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    # Ambil skor dan bersihkan state kuis
    final_score = session.pop("quiz_score", 0)
    session.pop("quiz_questions", None)
    session.pop("quiz_index", None)
    
    user_id = session.get("user_id")

    # Update skor jika skor baru lebih tinggi dari skor yang sudah tersimpan
    conn = sqlite3.connect(DB_USER)
    cursor = conn.cursor()
    cursor.execute("SELECT score FROM users WHERE id = ?", (user_id,))
    current_best_score = cursor.fetchone()[0]

    if final_score > current_best_score:
        cursor.execute("UPDATE users SET score = ? WHERE id = ?", (final_score, user_id))
        flash_message = f"Kuis selesai! Skor akhir Anda adalah {final_score}. Anda berhasil mencetak skor terbaik baru!"
    else:
        flash_message = f"Kuis selesai! Skor akhir Anda adalah {final_score}. Skor terbaik Anda tetap {current_best_score}."

    conn.commit()
    conn.close()
    
    # Simpan skor ini di session sementara untuk ditampilkan di leaderboard
    session['last_quiz_score'] = final_score

    flash(flash_message, "success")
    return redirect(url_for("leaderboard"))