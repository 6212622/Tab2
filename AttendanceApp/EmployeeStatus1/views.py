from django.shortcuts import render
from django.http import HttpResponse
from .models import Employee
from employee_data.models import ShiftSchedule
from datetime import datetime
from django.db import connection

# Хранение списка введенных сотрудников
employee_list = []

def employee_status(request):
    global employee_list
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        if not card_number:
            print("Номер карты не введен")
            return HttpResponse("Номер карты не введен")

        last_four_digits = card_number[-4:]
        print(f"Получен номер карты: {card_number}, последние четыре цифры: {last_four_digits}")

        try:
            employees = Employee.find_by_last_four_digits(last_four_digits)
            if not employees:
                print("Сотрудник не найден")
                context = {
                    'employee_list': employee_list,
                    'not_found': True
                }
                return render(request, 'employee_status.html', context)

            # Предполагаем, что возвращается одна запись
            employee_data = employees[0]
            employee = Employee(OwnerName=employee_data[0], ProcessedCodeP=employee_data[1], tabnumber=employee_data[2])
            print(f"Найден сотрудник: {employee.OwnerName}, табельный номер: {employee.tabnumber}, ProcessedCodeP: {employee.ProcessedCodeP}")
            current_date = datetime.now().date()
            current_time = datetime.now().time()
            print(f"Текущая дата: {current_date}, текущее время: {current_time}")

            # Получаем расписание сотрудника из таблицы EmployeeSchedule
            with connection.cursor() as cursor:
                cursor.execute("SELECT FullName, Schedule, TabNumber FROM tabel.dbo.EmployeeSchedule WHERE TabNumber = %s", [employee.tabnumber])
                schedule_row = cursor.fetchone()

            if schedule_row:
                schedule = str(schedule_row[1])  # Преобразуем в строку, если это не строка
                if len(schedule) < 2 and schedule == '3':
                    shift = schedule  # Первая цифра 3
                    brigade = 0  
                    print(f"Расписание сотрудника: смена {shift}, бригада {brigade}")
                else:
                    shift = schedule[0]  # Первая цифра - номер смены
                    brigade = schedule[1]  # Вторая цифра - номер бригады
                    print(f"Расписание сотрудника: смена {shift}, бригада {brigade}")

                # Получаем расписание смен на текущую дату
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM tabel.dbo.employee_data_shiftschedule WHERE date = %s", [current_date])
                    shift_schedule_row = cursor.fetchone()

                if shift_schedule_row:
                    shift_schedule = ShiftSchedule.objects.get(date=current_date)
                    print(f"Найдено расписание на текущую дату: {shift_schedule}")

                    # Определяем текущую смену
                    current_shift = None
                    if current_time >= datetime.strptime('20:00', '%H:%M').time() or current_time < datetime.strptime('08:00', '%H:%M').time():
                        current_shift = 'ночь'
                    elif current_time >= datetime.strptime('08:00', '%H:%M').time() and current_time < datetime.strptime('20:00', '%H:%M').time():
                        current_shift = 'день'
                    print(f"Текущая смена: {current_shift}")

                    # Сопоставление смен и бригад
                    shift_mapping = {
                        ('2', '1'): shift_schedule.shift_2_brigade_1,
                        ('2', '2'): shift_schedule.shift_2_brigade_2,
                        ('2', '3'): shift_schedule.shift_2_brigade_3,
                        ('2', '4'): shift_schedule.shift_2_brigade_4,
                    }

                    current_brigade_shift = shift_mapping.get((shift, brigade))
                    print(f"Текущая смена бригады: {current_brigade_shift}")

                    # Проверяем, находится ли сотрудник в текущей смене
                    if shift == '3':
                        if current_date.weekday() >= 5:  # Суббота и воскресенье
                            status = 'не работает'
                        else:
                            status = 'работает'
                    else:
                        status = 'работает' if current_shift == current_brigade_shift else 'не работает'
                    print(f"Статус сотрудника: {status}")

                    # Добавляем сотрудника в список
                    employee_list.append({
                        'tabnumber': employee.tabnumber,
                        'OwnerName': employee.OwnerName,
                        'status': status
                    })

                    context = {
                        'employee': employee,
                        'status': status,
                        'current_shift': current_shift,
                        'current_brigade_shift': current_brigade_shift,
                        'current_date': current_date,
                        'current_time': current_time,
                        'employee_list': employee_list,
                        'shift_schedule': shift_schedule,
                        'shift': shift
                    }
                    print(f"Контекст для шаблона: {context}")
                    return render(request, 'employee_status.html', context)
                else:
                    print("❌ Расписание на текущую дату не найдено")
                    return HttpResponse("Расписание на текущую дату не найдено")
            else:
                print("❌ Расписание сотрудника не найдено")
                return HttpResponse("Расписание сотрудника не найдено")
        except ShiftSchedule.DoesNotExist:
            print("Расписание на текущую дату не найдено")
            return HttpResponse("Расписание на текущую дату не найдено")
    print("Метод запроса не POST, отображение пустой формы")
    return render(request, 'employee_status.html', {'employee_list': employee_list})