from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count
from datetime import datetime, timedelta
from EmployeeStatus1.views import employee_list  # Используем данные из employee_list
import openpyxl
from openpyxl.styles import Alignment
from EmployeeStatus1.models import Report

def daily_report(request):
    # Ежедневный отчет
    today = datetime.now().date()
    daily_data = [emp for emp in employee_list if emp['status'] == 'работает' and emp['date'] == today]

    return render(request, 'reports/daily_report.html', {'daily_data': daily_data, 'today': today})


def monthly_report(request):
    # Ежемесячный отчет
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Генерация данных для таблицы
    monthly_data = {}
    for emp in employee_list:
        if emp['status'] == 'работает' and emp['date'].month == current_month and emp['date'].year == current_year:
            if emp['tabnumber'] not in monthly_data:
                monthly_data[emp['tabnumber']] = {'name': emp['OwnerName'], 'days': [0] * 31}
            monthly_data[emp['tabnumber']]['days'][emp['date'].day - 1] = 1

    return render(request, 'reports/monthly_report.html', {'monthly_data': monthly_data, 'current_month': current_month})


def export_to_excel(request):
    # Экспорт в Excel
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Создаем Excel-файл
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Отчет {current_month}-{current_year}"

    # Заголовки
    ws.append(["Табельный номер", "ФИО"] + [f"День {i}" for i in range(1, 32)])

    # Данные
    for emp in employee_list:
        row = [emp['tabnumber'], emp['OwnerName']] + emp['days']
        ws.append(row)

    # Стилизация
    for col in ws.columns:
        for cell in col:
            cell.alignment = Alignment(horizontal='center', vertical='center')

    # Сохранение файла
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="monthly_report_{current_month}_{current_year}.xlsx"'
    wb.save(response)
    return response


def index(request):
    # Получаем текущую дату
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Если метод POST, получаем выбранную дату
    if request.method == 'POST':
        selected_date = request.POST.get('selected_date', current_date)
    else:
        selected_date = current_date

    # Фильтруем отчеты по выбранной дате
    reports = Report.objects.filter(date=selected_date).order_by('-date')

    context = {
        'reports': reports,
        'current_date': selected_date,
    }
    return render(request, 'reports/index.html', context)
