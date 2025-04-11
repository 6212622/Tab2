from datetime import datetime
from EmployeeStatus1.models import Report

def get_daily_report():
    today = datetime.now().date()
    # Получаем данные из модели Report за текущий день
    reports = Report.objects.filter(date=today).order_by('tabnumber')
    return reports