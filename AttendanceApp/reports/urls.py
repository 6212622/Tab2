from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='reports_index'),
    path('daily/', views.daily_report_view, name='daily_report'),
    path('monthly/', views.monthly_report_view, name='monthly_report'),
    path('export/', views.export_to_excel, name='export_to_excel'),
]