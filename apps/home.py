from flask import request, session, render_template, redirect, url_for
from .__init__ import app, cities
from datetime import datetime, timedelta

@app.route("/")
def mainhome():
    return redirect(url_for('home'))

@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        city = request.form.get("city")

        today = datetime.today()
        days = ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"]

        weather = []
        for i in range(3):
            date = today + timedelta(days=i)
            weather.append({
                "day": days[date.weekday()],
                "date": date.strftime("%d-%m-%Y"),
                "day_temp": 28 + i, 
                "night_temp": 22 + i  
            })

        return render_template("home.html",
                               city=city,
                               cities=cities,
                               weather=weather)

    return render_template("home.html", cities=cities, weather=None)