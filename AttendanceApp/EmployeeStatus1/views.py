from django.shortcuts import render
from django.http import HttpResponse
from .models import Employee, Report
from employee_data.models import ShiftSchedule
from datetime import datetime
from django.db import connections, connection
import base64
from django.shortcuts import render
from .models import Report
from django.http import HttpResponseBadRequest
from datetime import datetime
import locale
from babel.dates import format_date

# Устанавливаем локаль на русский
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

# Хранение списка введенных сотрудников
employee_list = []

def employee_status(request):
    global employee_list
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        if not card_number:
            print("Номер карты не введен")
            return HttpResponse("Номер карты не введен")

        # Проверка: табельный номер или номер карты
        if len(card_number) > 4:
            last_four_digits = card_number[-4:]
            print(f"Получен номер карты: {card_number}, последние четыре цифры: {last_four_digits}")
            employee_data = Employee.find_by_last_four_digits(last_four_digits)
            if not employee_data:
                print("Сотрудник не найден")
                context = {
                    'employee_list': employee_list,
                    'not_found': True
                }
                return render(request, 'employee_status.html', context)
            else:
                employee = Employee(
                    OwnerName=employee_data[0][0],  # Используем данные из employee_data
                    ProcessedCodeP=employee_data[0][1],  # Неизвестно, что это за поле, оставляем 0
                    tabnumber=employee_data[0][2]
                )
        else:
            employee_data = Employee.find_by_tabnumber(card_number)  # Сохраняем результат в employee_data
            if not employee_data:
                print("Сотрудник не найден")
                context = {
                    'employee_list': employee_list,
                    'not_found': True
                }
                return render(request, 'employee_status.html', context)

            # Создаем объект Employee
            else:
                employee = Employee(
                OwnerName=employee_data['fio'],  # Используем данные из employee_data
                ProcessedCodeP=0,  # Неизвестно, что это за поле, оставляем 0
                tabnumber=employee_data['tabnumber']
                )
        print(f"Найден сотрудник: {employee.OwnerName}, табельный номер: {employee.tabnumber}")

        try:
            # Предполагаем, что возвращается одна запись
            print(f"Найден сотрудник: {employee.OwnerName}, табельный номер: {employee.tabnumber}, ProcessedCodeP: {employee.ProcessedCodeP}")
            current_date = datetime.now().date()
            current_time = datetime.now().time()
            print(f"Текущая дата: {current_date}, текущее время: {current_time}")
        
            # Получаем расписание сотрудника из таблицы smeny1c
            with connections['test_db'].cursor() as cursor:
                cursor.execute("SELECT tabnumber, smena FROM Test.dbo.smeny1c WHERE tabnumber = %s", [employee.tabnumber])
                smeny_row = cursor.fetchone()
            
            if smeny_row:
                smena = smeny_row[1]
                print(f"Смена и бригада из таблицы smeny1c: {smena}")

                # Определяем смену и бригаду
                shift = None
                brigade = None

                if "График сменности №1 (Бригада 1)" in smena:
                    shift = '1'
                    brigade = '1'
                elif "График сменности №1 (Бригада 2)" in smena:
                    shift = '1'
                    brigade = '2'
                elif "График сменности №2 (Бригада 1)" in smena:
                    shift = '2'
                    brigade = '1'
                elif "График сменности №2 (Бригада 2)" in smena:
                    shift = '2'
                    brigade = '2'
                elif "График сменности №2 (Бригада 3)" in smena:
                    shift = '2'
                    brigade = '3'
                elif "График сменности №2 (Бригада 4)" in smena:
                    shift = '2'
                    brigade = '4'
                elif "Пятидневка рабочая неделя" in smena or "Пятидневная рабочая неделя" in smena:
                    shift = '3'
                    brigade = None
                else:
                    print("Неизвестный график сменности")

                print(f"Определены смена: {shift}, бригада: {brigade}")


                # Проверяем статус сотрудника
                if shift == '3':
                    if current_date.weekday() >= 5:  # Суббота и воскресенье
                        status = 'не работает'
                    else:
                        status = 'работает'
                else:
                    # Сопоставление смен и бригад
                    shift_mapping = {
                        ('2', '1'): 'Бригада 1',
                        ('2', '2'): 'Бригада 2',
                        ('2', '3'): 'Бригада 3',
                        ('2', '4'): 'Бригада 4',
                    }
                    print(f"Текущая смена: {shift_mapping.get((shift, brigade))}")
                    # Получаем расписание смен на текущую дату
                    current_brigade_shift = shift_mapping.get((shift, brigade))
                    status = 'работает' if current_brigade_shift else 'не работает'

                    print(f"Статус сотрудника: {status}")
            else:
                print("Смена и бригада не найдены в таблице smeny1c")
                shift = None
                brigade = None
                status = 'неизвестно'

            if smeny_row:
                schedule = str(smeny_row[1])  # Преобразуем в строку, если это не строка
                if len(schedule) < 2 and schedule == '3':
                    # shift = schedule  # Первая цифра 3
                    # brigade = 0  
                    print(f"Расписание сотрудника: смена {shift}, бригада {brigade}")
                else:
                    # shift = schedule[0]  # Первая цифра - номер смены
                    # brigade = schedule[1]  # Вторая цифра - номер бригады
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

                    # Получаем фото сотрудника из базы данных
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT Picture FROM OrionTMZ.dbo.pList WHERE TabNumber = %s", [employee.tabnumber])
                        row = cursor.fetchone()

                    if row:
                        binary_data = row[0]  # Получаем бинарные данные
                        photo_base64 = base64.b64encode(binary_data).decode('utf-8')  # Преобразуем в base64 для отображения в HTML
                        print("✅ Файл успешно декодирован!")
                    else:
                        print("❌ Данные не найдены")
                        photo_base64 = None

                    # Проверяем, есть ли запись в отчете на текущую дату
                    report_exists = Report.objects.filter(tabnumber=employee.tabnumber, date=current_date).exists()
                    if report_exists or status == 'не работает':
                        print("Повторный ввод")
                        status = 'повторный ввод'
                    else:
                        # Сохраняем запись в отчет
                        Report.objects.create(
                            tabnumber=employee.tabnumber,
                            owner_name=employee.OwnerName,
                            shift=shift,
                            brigade=brigade,
                            date=current_date,
                            status=status
                        )

                    # Добавляем сотрудника в список
                    employee_list.append({
                        'tabnumber': employee.tabnumber,
                        'OwnerName': employee.OwnerName,
                        'status': status
                    })

                    # Получаем текущую дату
                    current_date = datetime.now()

                    # Форматируем дату на русском языке
                    formatted_date = format_date(current_date, format='d MMMM y', locale='ru')
                    print(f"Дата: {formatted_date}")

                    context = {
                        'employee': employee,
                        'status': status,
                        'current_shift': current_shift,
                        'current_brigade_shift': current_brigade_shift,
                        'current_date': formatted_date,
                        'current_time': current_time,
                        'employee_list': employee_list,
                        'shift_schedule': shift_schedule,
                        'shift': shift,
                        'photo': photo_base64  # Добавляем фото в контекст
                    }
                    print(f"Контекст для шаблона: {context}")
                    return render(request, 'employee_status.html', context)
                else:
                    print("❌ Расписание на текущую дату не найдено")
                    return HttpResponse("Расписание на текущую дату не найдено")
            
        except ShiftSchedule.DoesNotExist:
            print("Расписание на текущую дату не найдено")
            return HttpResponse("Расписание на текущую дату не найдено")
    print("Метод запроса не POST, отображение пустой формы")
    return render(request, 'employee_status.html', {'employee_list': employee_list})



def report_view(request):
    reports = Report.objects.all().order_by('-date')
    if request.method == 'POST':
        date_range = request.POST.get('date_range')
        selected_date = request.POST.get('selected_date')

        # Если дата не указана, берем сегодняшнюю дату
        if date_range == 'day':
            if not selected_date:
                selected_date = datetime.now().strftime('%Y-%m-%d')  # Текущая дата в формате YYYY-MM-DD
            try:
                reports = Report.objects.filter(date=selected_date).order_by('-date')
            except ValueError:
                return HttpResponseBadRequest("Неверный формат даты. Убедитесь, что дата указана в формате YYYY-MM-DD.")
        elif date_range == 'month':
            selected_month = request.POST.get('selected_month')
            if not selected_month:
                selected_month = datetime.now().strftime('%Y-%m')  # Текущий месяц в формате YYYY-MM
            year, month = selected_month.split('-')
            reports = Report.objects.filter(date__year=year, date__month=month).order_by('-date')
        elif date_range == 'year':
            selected_year = request.POST.get('selected_year')
            if not selected_year:
                selected_year = datetime.now().strftime('%Y')  # Текущий год
            reports = Report.objects.filter(date__year=selected_year).order_by('-date')

    return render(request, 'report1.html', {'reports': reports})

