from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
import mysql.connector as sql
from mysql.connector import IntegrityError

@csrf_protect
def signaction(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        phone = request.POST.get("phone_number", "").strip()
        address = request.POST.get("address", "").strip()
        password = request.POST.get("password", "").strip()

        if not all([full_name, phone, address, password]):
            return render(request, "customer/signup_page.html", {
                "error": "All fields are required.",
                "form": request.POST
            })

        hashed_password = make_password(password)

        try:
            conn = sql.connect(
                host="localhost",
                user="root",
                password="651sc32y@",
                database="website"
            )
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO customers (full_name, phone_number, address, password)
                VALUES (%s, %s, %s, %s)
            """, (full_name, phone, address, hashed_password))

            conn.commit()

        except IntegrityError:
            # ✅ THIS HANDLES DUPLICATE PHONE NUMBERS
            return render(request, "customer/signup_page.html", {
                "error": "This phone number is already registered. Please login.",
                "form": request.POST
            })

        except Exception as e:
            return render(request, "customer/signup_page.html", {
                "error": f"Database error: {e}",
                "form": request.POST
            })

        finally:
            try: cur.close()
            except: pass
            try: conn.close()
            except: pass

        messages.success(request, "Signup successful! Please login.")
        return redirect("customer_login:login")

    return render(request, "customer/signup_page.html")
