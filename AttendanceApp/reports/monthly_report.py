from datetime import datetime
from EmployeeStatus1.models import Report

def get_monthly_report(month=None, year=None):
    current_date = datetime.now()
    current_month = month or current_date.month
    current_year = year or current_date.year
    # Получаем данные из модели Report за указанный месяц и год
    reports = Report.objects.filter(date__year=current_year, date__month=current_month).order_by('tabnumber', 'date')
    return reports