from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_status, name='employee_status'),
    path('report/', views.report_view, name='report_view'),
]