from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Farmer
    path('', include(('farmer.signup.urls', 'farmer_signup'), namespace='farmer_signup')),
    path('farmer/login/', include(('farmer.login.urls', 'farmer_login'), namespace='farmer_login')),

    # Customer
    path('customer/signup/', include(('customer.signup.urls', 'customer_signup'), namespace='customer_signup')),
    path('customer/login/', include(('customer.login.urls', 'customer_login'), namespace='customer_login')),
]
