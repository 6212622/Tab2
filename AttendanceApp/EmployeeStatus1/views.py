from django.shortcuts import render
from django.http import HttpResponse
from .models import Employee
from employee_data.models import ShiftSchedule  # Измените импорт на относительный
from datetime import datetime

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
            shift_schedule = ShiftSchedule.objects.get(date=current_date)
            print(f"Найдено расписание на текущую дату: {shift_schedule}")

            # Определяем текущую смену
            current_shift = None
            if current_time >= datetime.strptime('20:00', '%H:%M').time() or current_time < datetime.strptime('08:00', '%H:%M').time():
                current_shift = 'ночь'
            elif current_time >= datetime.strptime('08:00', '%H:%M').time() and current_time < datetime.strptime('20:00', '%H:%M').time():
                current_shift = 'день'
            print(f"Текущая смена: {current_shift}")

            # Проверяем, находится ли сотрудник в текущей смене
            status = 'не работает'
            if current_shift == 'ночь' and (shift_schedule.shift_2_brigade_1 == 'ночь' or shift_schedule.shift_2_brigade_2 == 'ночь' or shift_schedule.shift_2_brigade_3 == 'ночь' or shift_schedule.shift_2_brigade_4 == 'ночь'):
                status = 'работает'
            elif current_shift == 'день' and (shift_schedule.shift_2_brigade_1 == 'день' or shift_schedule.shift_2_brigade_2 == 'день' or shift_schedule.shift_2_brigade_3 == 'день' or shift_schedule.shift_2_brigade_4 == 'день'):
                status = 'работает'
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
                'current_date': current_date,
                'current_time': current_time,
                'employee_list': employee_list
            }
            print(f"Контекст для шаблона: {context}")
            return render(request, 'employee_status.html', context)
        except ShiftSchedule.DoesNotExist:
            print("Расписание на текущую дату не найдено")
            return HttpResponse("Расписание на текущую дату не найдено")
    print("Метод запроса не POST, отображение пустой формы")
    return render(request, 'employee_status.html', {'employee_list': employee_list})