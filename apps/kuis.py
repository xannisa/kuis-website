from flask import request, session, flash, redirect, url_for, render_template
from .__init__ import app, db_user, db_soal, get_db_connection


@app.route("/kuis_start")
def kuis_start():
    """Menginisialisasi state kuis: mengambil 5 soal acak dan reset skor."""
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection(db_soal)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM questions ORDER BY RAND() LIMIT 5") 
    question_ids = [row[0] for row in cursor.fetchall()]
    conn.close()

    if not question_ids:
        return redirect(url_for("home"))

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

    if questions is None or index is None:
        return redirect(url_for("kuis_start"))

    if request.method == "POST":
        qid_from_form = request.form.get("qid")
        answer = request.form.get("answer")

        if not answer:
            return redirect(url_for("kuis"))
        
        conn = get_db_connection(db_soal)
        cursor = conn.cursor()

        cursor.execute("SELECT correct_answer FROM questions WHERE id = %s", (qid_from_form,))
        correct_answer = cursor.fetchone()[0]
        conn.close()

        if answer == correct_answer:
            session["quiz_score"] = session["quiz_score"] + 1
        else:
            pass

        session["quiz_index"] = index + 1
        index = session["quiz_index"] 

        if index >= len(questions):
            return redirect(url_for("kuis_result"))

        return redirect(url_for("kuis"))

    if index >= len(questions):
        return redirect(url_for("kuis_result"))

    current_qid = questions[index]

    conn = get_db_connection(db_soal)
    cursor = conn.cursor()
    cursor.execute("SELECT id, question, option_a, option_b, option_c, option_d FROM questions WHERE id = %s", (current_qid,))
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
    
    is_last_question = (index + 1) == len(questions)

    return render_template("kuis.html",
                           q=question,
                           index=index + 1,
                           total=len(questions),
                           is_last_question=is_last_question)


@app.route("/kuis_result")
def kuis_result():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    final_score = session.pop("quiz_score", 0)
    session.pop("quiz_questions", None)
    session.pop("quiz_index", None)
    
    user_id = session.get("user_id")

    conn = get_db_connection(db_user)
    cursor = conn.cursor()
    cursor.execute("SELECT score FROM users WHERE id = %s", (user_id,))
    current_best_score = cursor.fetchone()[0]

    if final_score > current_best_score:
        cursor.execute("UPDATE users SET score = %s WHERE id = %s", (final_score, user_id))
        flash_message = f"Kuis selesai! Skor akhir Anda adalah {final_score}. Anda berhasil mencetak skor terbaik baru!"
    else:
        flash_message = f"Kuis selesai! Skor akhir Anda adalah {final_score}. Skor terbaik Anda tetap {current_best_score}."

    conn.commit()
    conn.close()
    session['last_quiz_score'] = final_score

    return redirect(url_for("leaderboard"))