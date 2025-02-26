from django.urls import path
from .views import employee_status

urlpatterns = [
    path('', employee_status, name='employee_status'),
]