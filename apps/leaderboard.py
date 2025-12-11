from flask import request, session, render_template
from .__init__ import app, db_user, get_db_connection
import sqlite3

@app.route("/leaderboard")
def leaderboard():
    conn = get_db_connection(db_user)
    cursor = conn.cursor()

    # ambil data username dan score, urutkan dari tertinggi
    cursor.execute("SELECT username, score FROM users ORDER BY score DESC")
    users = cursor.fetchall()
    conn.close()

    # convert ke list of dict untuk Jinja2
    leaderboard_data = [{"username": u[0], "score": u[1]} for u in users]
    
    # Ambil skor terakhir jika ada di session (untuk ditampilkan di leaderboard.html)
    last_score = session.pop('last_quiz_score', None)

    return render_template("leaderboard.html", users=leaderboard_data, last_score=last_score)

# ... (setelah fungsi leaderboard)