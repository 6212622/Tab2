from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('employee_data/', include('employee_data.urls')),
    path('employee_status/', include('EmployeeStatus1.urls')),
]