from django.shortcuts import render
from employee_data.cal import calculate_work_time_for_month

def employee_report(request):
    report = None
    non_empty_days = []
    empty_days = []
    error = None
    days = []

    if request.method == 'GET':
        tabnumber = request.GET.get('tabnumber')
        month = request.GET.get('month')
        year = request.GET.get('year')

        if not tabnumber or not month or not year:
            return render(request, 'report.html', {'report': None, 'days': [], 'error': None})

        try:
            tabnumber = int(tabnumber)
            month = int(month)
            year = int(year)

            print(f"Данные из формы: tabnumber={tabnumber}, month={month}, year={year}")
            print(f"Типы данных: tabnumber={type(tabnumber)}, month={type(month)}, year={type(year)}")

            report, non_empty_days, empty_days = calculate_work_time_for_month(tabnumber, month, year)
            print(f"Отчет, полученный из функции: {report}")

            # Объединение и сортировка дней
            days = [{'day': day, 'time': report['times'][report['days'].index(day)]} for day in non_empty_days] + [{'day': day, 'time': '0ч.0м.'} for day in empty_days]
            days.sort(key=lambda x: x['day'])

        except ValueError:
            error = "Пожалуйста, введите корректные числовые значения для всех полей."
            print(error)
        except Exception as e:
            print(f"Типы данных: tabnumber={type(tabnumber)}, month={type(month)}, year={type(year)}")
            error = f"Ошибка при создании отчёта: {e}"
            print(error)

    return render(request, 'report.html', {'report': report, 'days': days, 'error': error})