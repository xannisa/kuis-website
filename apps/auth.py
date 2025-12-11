from flask import request, redirect, url_for, render_template, flash, session
from .__init__ import app, get_db_connection, db_user
#import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm_password")

        # 1️⃣ Check if passwords match
        if password != confirm:
            flash("Passwords do not match!")
            return redirect(url_for("register"))

        conn = get_db_connection(db_user)
        cursor = conn.cursor()

        # 2️⃣ Check for duplicate username
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            flash("Username already exists!")
            conn.close()
            return redirect(url_for("register"))

        # 3️⃣ Check for duplicate email
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            flash("Email already exists!")
            conn.close()
            return redirect(url_for("register"))

        # 4️⃣ Hash password
        hashed_pw = generate_password_hash(password)

        # 5️⃣ Insert new user
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_pw)
        )
        conn.commit()
        conn.close()

        # 6️⃣ Success → go to login page
        flash("Registration successful! Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection(db_user)
        cursor = conn.cursor()
        #
        # 1️⃣ Cari user berdasarkan username
        cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()

        # 2️⃣ Jika user tidak ditemukan
        if not user:
            flash("Username not found!")
            return redirect(url_for("login"))

        user_id = user[0]
        hashed_pw = user[1]

        # 3️⃣ Cek password
        if not check_password_hash(hashed_pw, password):
            flash("Incorrect password!")
            return redirect(url_for("login"))

        # 4️⃣ Jika benar → masukkan user_id ke session
        session["user_id"] = user_id
        session["username"] = username

        return redirect(url_for("leaderboard"))   # ganti ke halaman tujuanmu

    return render_template("login.html")

@app.route("/logout")
def logout():
    # Cek apakah pengguna sedang login
    if "user_id" in session:
        # Hapus semua item terkait sesi pengguna
        session.pop("user_id", None)
        session.pop("username", None)
        # flash("Anda telah berhasil keluar.", "success") <--- DIHAPUS
    
    # Arahkan ke halaman login.html
    return redirect(url_for("login"))