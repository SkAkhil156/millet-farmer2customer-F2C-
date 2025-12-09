# login/views.py
from django.shortcuts import render, redirect
import mysql.connector as sql
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse, NoReverseMatch

@csrf_exempt
def loginaction(request):
    """
    Login view: accept either email (preferred) or first_name as identity.
    On success set session['user_id'] and redirect to URL named 'welcome'.
    """
    if request.method == "POST":
        identity = (request.POST.get('identity') or request.POST.get('email') or '').strip()
        password = request.POST.get('password', '').strip()

        if not identity or not password:
            return render(request, 'login_page.html', {
                'error': 'Please enter email (or first name) and password.',
                'identity': identity
            })

        conn = None
        cursor = None
        try:
            conn = sql.connect(host="localhost", user="root", password="651sc32y@", database='website')
            cursor = conn.cursor(dictionary=True)

            user = None

            # Try matching by email (case-insensitive)
            try:
                cursor.execute("SELECT * FROM farmers WHERE LOWER(email) = %s LIMIT 1", (identity.lower(),))
                user = cursor.fetchone()
            except Exception:
                user = None

            # If not found by email, try by first_name (exact match)
            if not user:
                cursor.execute("SELECT * FROM farmers WHERE first_name = %s LIMIT 1", (identity,))
                user = cursor.fetchone()

            if not user:
                return render(request, 'login_page.html', {
                    'error': 'Invalid credentials.',
                    'identity': identity
                })

            stored_hash = user.get('password')
            if not stored_hash:
                return render(request, 'login_page.html', {
                    'error': 'User has no password. Contact admin.',
                    'identity': identity
                })

            if check_password(password, stored_hash):
                # Successful login -> set session values
                request.session['user_id'] = user.get('id')
                request.session['first_name'] = user.get('first_name')

                # Try to redirect to the named URL 'welcome'
                try:
                    return redirect('welcome')
                except NoReverseMatch:
                    # Fallback: render welcome template directly if redirect fails
                    return render(request, 'welcome.html', {'user': user})

            else:
                return render(request, 'login_page.html', {
                    'error': 'Invalid credentials.',
                    'identity': identity
                })

        except Exception as e:
            return render(request, 'login_page.html', {'error': f'Login error: {e}', 'identity': identity})
        finally:
            if cursor:
                try: cursor.close()
                except Exception: pass
            if conn:
                try: conn.close()
                except Exception: pass

    # GET -> show login form
    return render(request, 'login_page.html')


# Simple welcome view (add this in the same file)
def welcome(request):
    """
    Minimal welcome view — shows first name from session if present.
    """
    first = request.session.get('first_name')
    return render(request, 'welcome.html', {'first_name': first})
