# signup/views.py
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
import mysql.connector as sql
from mysql.connector import IntegrityError
import logging

logger = logging.getLogger(__name__)

@csrf_protect
def signaction(request):
    """
    Sign-up view that requires farmer_type (matches DB).
    Returns clear message listing any missing required fields.
    """
    if request.method == "POST":
        # gather fields
        fn = request.POST.get('first_name', '').strip()
        ln = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        gender = request.POST.get('gender', '').strip()
        farmer_type = request.POST.get('farmer_type', '').strip()
        password = request.POST.get('password', '').strip()
        address = request.POST.get('address', '').strip()
        farm_name = request.POST.get('farm_name', '').strip() or None
        land_area = request.POST.get('land_area', '').strip()
        crops = request.POST.get('crops', '').strip()
        certification = request.POST.get('certification', '').strip()

        fields = {
            'first_name': fn,
            'last_name': ln,
            'email': email,
            'gender': gender,
            'farmer_type': farmer_type,
            'password': password,
            'address': address,
            'land_area': land_area,
            'crops': crops,
            'certification': certification
        }

        missing = [name for name, val in fields.items() if not val]
        if missing:
            friendly = {
                'first_name': 'First name', 'last_name': 'Last name', 'email': 'Email',
                'gender': 'Gender', 'farmer_type': 'Farmer type', 'password': 'Password',
                'address': 'Address', 'land_area': 'Land area', 'crops': 'Crops',
                'certification': 'Certification'
            }
            missing_friendly = ', '.join(friendly.get(m, m) for m in missing)
            logger.debug("Signup missing fields: %s", missing)
            return render(request, 'signup_page.html', {
                'error': f'Please fill all required fields: {missing_friendly}.',
                'form': request.POST
            })

        hashed_password = make_password(password)

        conn = None
        cursor = None
        try:
            conn = sql.connect(host="localhost", user="root", password="651sc32y@", database='website')
            cursor = conn.cursor(dictionary=True)

            # Check duplicate email
            cursor.execute("SELECT id FROM farmers WHERE LOWER(email) = %s LIMIT 1", (email,))
            if cursor.fetchone():
                return render(request, 'signup_page.html', {
                    'error': 'Email already registered. Please use a different email or login.',
                    'form': request.POST
                })

            insert_query = """
                INSERT INTO farmers (
                    first_name, last_name, email, gender, farmer_type, password,
                    address, farm_name, land_area, crops, certification
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                fn, ln, email, gender, farmer_type, hashed_password,
                address, farm_name, land_area, crops, certification
            )
            cursor.execute(insert_query, params)
            conn.commit()

        except IntegrityError as ie:
            logger.exception("IntegrityError during signup")
            return render(request, 'signup_page.html', {'error': f'Integrity error: {ie}', 'form': request.POST})
        except Exception as e:
            logger.exception("Database error during signup")
            return render(request, 'signup_page.html', {'error': f'Database error: {e}', 'form': request.POST})
        finally:
            if cursor:
                try: cursor.close()
                except Exception: pass
            if conn:
                try: conn.close()
                except Exception: pass

        messages.success(request, "Registration successful. Please login.")
        return redirect('login')

    return render(request, 'signup_page.html')
