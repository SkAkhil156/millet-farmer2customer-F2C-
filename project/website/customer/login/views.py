from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
import mysql.connector as sql

def loginaction(request):
    if request.method == "POST":
        name = request.POST.get("identity")
        password = request.POST.get("password")

        conn = sql.connect(host="localhost", user="root", password="651sc32y@", database="website")
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM customers WHERE full_name=%s", (name,))
        user = cur.fetchone()
        conn.close()

        if user and check_password(password, user["password"]):
            request.session["customer_name"] = user["full_name"]
            return redirect("customer_login:welcome")

        return render(request, "customer/login_page.html", {"error": "Invalid login"})

    return render(request, "customer/login_page.html")

def welcome(request):
    return render(request, "customer/welcome.html", {
        "customer_name": request.session.get("customer_name")
    })
