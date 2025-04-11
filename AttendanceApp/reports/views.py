from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count
from datetime import datetime, timedelta
from calendar import monthrange
from EmployeeStatus1.views import employee_list  # Используем данные из employee_list
import openpyxl
from openpyxl.styles import Alignment
from EmployeeStatus1.models import Report
from .daily_report import get_daily_report
from .monthly_report import get_monthly_report

def daily_report_view(request):
    reports = get_daily_report()
    return render(request, 'reports/daily_report.html', {'reports': reports})

def monthly_report_view(request):
    selected_month = request.GET.get('month')
    selected_year = request.GET.get('year')

    if selected_month and selected_year:
        try:
            month = int(selected_month)
            year = int(selected_year)
        except ValueError:
            return HttpResponse("Неверный формат месяца или года.")
    else:
        # Если месяц и год не указаны, используем текущие
        current_date = datetime.now()
        month = current_date.month
        year = current_date.year

    # Получаем отчеты за указанный месяц и год
    reports = get_monthly_report(month=month, year=year)

    # Получаем количество дней в месяце
    days_in_month = monthrange(year, month)[1]
    dates = [f"{day:02d}.{month:02d}.{year}" for day in range(1, days_in_month + 1)]

    # Подготавливаем данные для таблицы
    employees = {}
    daily_totals = [0] * days_in_month  # Инициализируем список для подсчета общей суммы по дням
    for report in reports:
        if report.tabnumber not in employees:
            employees[report.tabnumber] = {
                'fio': report.owner_name,
                'days': [''] * days_in_month  # Инициализируем пустыми значениями
            }
        day = report.date.day
        employees[report.tabnumber]['days'][day - 1] = '1'  # Отмечаем присутствие
        daily_totals[day - 1] += 1  # Увеличиваем счетчик для соответствующего дня

    # Преобразуем данные в список для удобства отображения
    employee_data = [
        {'tabnumber': tabnumber, 'fio': data['fio'], 'days': data['days']}
        for tabnumber, data in employees.items()
    ]

    return render(request, 'reports/monthly_report.html', {
        'employee_data': employee_data,
        'dates': dates,
        'selected_month': month,
        'selected_year': year,
        'months': list(range(1, 13)),
        'daily_totals': daily_totals,  # Передаем общую сумму по дням
    })

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
