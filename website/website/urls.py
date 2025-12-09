# website/urls.py
from django.contrib import admin
from django.urls import path
from signup.views import signaction
from login.views import loginaction

# import the welcome view from login.views (we added this earlier)
from login.views import welcome

# ADD THESE TWO IMPORTS ↓
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Signup page
    path('', signaction, name='home'),
    path('signup/', signaction, name='signup'),

    # Login page
    path('login/', loginaction, name='login'),

    # Welcome page (needed so redirect('welcome') works)
    path('welcome/', welcome, name='welcome'),
]

# THIS PART IS REQUIRED FOR SERVING UPLOADED FILES IN DEVELOPMENT
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
