from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
import mysql.connector as sql

def loginaction(request):
    if request.method == "POST":
        name = request.POST.get("identity")
        password = request.POST.get("password")

        conn = sql.connect(host="localhost", user="root", password="651sc32y@", database="website")
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM farmers WHERE full_name=%s", (name,))
        user = cur.fetchone()
        conn.close()

        if user and check_password(password, user["password"]):
            request.session["farmer_name"] = user["full_name"]
            return redirect("farmer_login:welcome")

        return render(request, "farmer/login_page.html", {"error": "Invalid login"})

    return render(request, "farmer/login_page.html")

def welcome(request):
    return render(request, "farmer/welcome.html", {
        "farmer_name": request.session.get("farmer_name")
    })
