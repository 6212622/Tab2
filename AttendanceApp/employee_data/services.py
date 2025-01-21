from django.shortcuts import render
from django.http import HttpResponseBadRequest
from datetime import datetime
from collections import defaultdict
from employee_data.cal import calculate_work_time_for_month
import logging
from datetime import date


logger = logging.getLogger(__name__)

def employee_report(request):
    logger.info(f"Request GET data: {request.GET}")
    # Получение параметров из формы
    tabnumber = int(request.GET.get("tabnumber"))
    month = int(request.GET.get("month"))
    year = int(request.GET.get("year"))

    print(f"Данные из формы: tabnumber={tabnumber}, month={month}, year={year}")

    # Проверка обязательных параметров
    if not (tabnumber and month and year):
        return HttpResponseBadRequest("Табельный номер, месяц и год обязательны для ввода!")

    try:
        tabnumber = int(tabnumber)
        month = int(month)
        year = int(year)
    except ValueError:
        return HttpResponseBadRequest("Неверные данные: табельный номер, месяц и год должны быть числами.")

    # Логика формирования отчета
    report = calculate_work_time_for_month(tabnumber, month, year)
    # Форматируем дату отчета

    report_date = date(year, month, 1).strftime("%d.%m.%Y")

    return render(request, 'report.html', {
        'month': month,
        'year': year,
        'tabnumber': tabnumber,
        'report': report
    })
