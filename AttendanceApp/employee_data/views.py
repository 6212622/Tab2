from django.shortcuts import render
from django.http import HttpResponse
from .services import fill_schedule_for_year
from .models import ShiftSchedule
from datetime import datetime

def fill_schedule(request):
    if request.method == 'POST':
        year = request.POST.get('year')
        shift_1_brigade_1 = request.POST.get('shift_1_brigade_1')
        shift_1_brigade_2 = request.POST.get('shift_1_brigade_2')
        shift_2_brigade_1 = request.POST.get('shift_2_brigade_1')
        shift_2_brigade_2 = request.POST.get('shift_2_brigade_2')
        shift_2_brigade_3 = request.POST.get('shift_2_brigade_3')
        shift_2_brigade_4 = request.POST.get('shift_2_brigade_4')
        print(f"Получен запрос на формирование расписания для года: {year}")
        try:
            year = int(year)
            start_date = datetime(year, 1, 1)
            print(f"Начальная дата: {start_date}")
            fill_schedule_for_year(start_date, shift_1_brigade_1, shift_1_brigade_2, shift_2_brigade_1, shift_2_brigade_2, shift_2_brigade_3, shift_2_brigade_4)
            schedule = ShiftSchedule.objects.filter(date__year=year)
            print(f"Сформированное расписание: {schedule}")
            return render(request, 'report.html', {'schedule': schedule, 'year': year})
        except ValueError:
            print("Ошибка: Неверный формат года.")
            return HttpResponse("Неверный формат года.")
    return render(request, 'report.html')