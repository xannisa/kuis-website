from flask import request, redirect, url_for, render_template, flash, session
from .__init__ import app, get_db_connection, db_user
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm_password")

        if password != confirm:
            return redirect(url_for("register"))

        conn = get_db_connection(db_user)
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            conn.close()
            return redirect(url_for("register"))

        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            conn.close()
            return redirect(url_for("register"))

        hashed_pw = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_pw)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection(db_user)
        cursor = conn.cursor()

        cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            return redirect(url_for("login"))

        user_id = user[0]
        hashed_pw = user[1]

        if not check_password_hash(hashed_pw, password):
            return redirect(url_for("login"))

        session["user_id"] = user_id
        session["username"] = username

        return redirect(url_for("leaderboard"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    if "user_id" in session:
        session.pop("user_id", None)
        session.pop("username", None)
    
    return redirect(url_for("login"))