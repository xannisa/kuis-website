from flask import request, session, render_template
from .__init__ import app, db_user, get_db_connection
import sqlite3

@app.route("/leaderboard")
def leaderboard():
    conn = get_db_connection(db_user)
    cursor = conn.cursor()

    cursor.execute("SELECT username, score FROM users ORDER BY score DESC")
    users = cursor.fetchall()
    conn.close()

    leaderboard_data = [{"username": u[0], "score": u[1]} for u in users]
    
    last_score = session.pop('last_quiz_score', None)

    return render_template("leaderboard.html", users=leaderboard_data, last_score=last_score)
