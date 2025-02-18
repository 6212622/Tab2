from django.urls import path
from .views import fill_schedule

urlpatterns = [
    path('fill_schedule/', fill_schedule, name='fill_schedule'),
]