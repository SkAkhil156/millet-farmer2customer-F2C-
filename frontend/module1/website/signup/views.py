from django.shortcuts import render, redirect
import mysql.connector as sql
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def signaction(request):
    # Show page on GET, handle insert on POST
    if request.method == "POST":
        fn = request.POST.get('first_name', '').strip()
        ln = request.POST.get('last_name', '').strip()
        sex = request.POST.get('sex', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        # Basic validation
        if not (fn and ln and sex and email and password):
            return render(request, 'signup/signup_page.html', {'error': 'Please fill all fields.'})

        try:
            conn = sql.connect(host="localhost", user="root", password="651sc32y@", database='website')
            cursor = conn.cursor()
            # Use parameterized query to avoid SQL injection
            query = "INSERT INTO users (first_name, last_name, sex, email, password) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (fn, ln, sex, email, password))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            # Return the template with an error message (use debug info only in dev)
            return render(request, 'signup/signup_page.html', {'error': str(e)})

        # After successful signup redirect to login page to avoid form re-submission
        return redirect('login')

    # GET
    return render(request, 'signup_page.html')

