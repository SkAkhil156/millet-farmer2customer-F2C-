from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
import mysql.connector as sql

def signaction(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone_number")
        address = request.POST.get("address")
        land = request.POST.get("land_size")
        crops = request.POST.get("crops")
        password = request.POST.get("password")

        hashed = make_password(password)

        conn = sql.connect(host="localhost", user="root", password="651sc32y@", database="website")
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO farmers (full_name, phone_number, address, land_size, crops, password) VALUES (%s,%s,%s,%s,%s,%s)",
            (full_name, phone, address, land, crops, hashed)
        )
        conn.commit()
        conn.close()

        return redirect("farmer_login:login")

    return render(request, "farmer/signup_page.html")
