from datetime import datetime, timedelta
from .models import ShiftSchedule

def fill_schedule_for_year(start_date, shift_1_brigade_1, shift_1_brigade_2, shift_2_brigade_1, shift_2_brigade_2, shift_2_brigade_3, shift_2_brigade_4):
    # Удаляем существующие записи для указанного года
    ShiftSchedule.objects.filter(date__year=start_date.year).delete()

    # Определяем смены и бригады
    shifts_1 = ["1 день", "2 день", "1 выходной", "2 выходной"]
    shifts_2 = ["ночь", "отсыпной", "выходной", "день"]

    # Проходим по каждому дню года
    for day in range(365):
        current_date = start_date + timedelta(days=day)
        shift_schedule = ShiftSchedule(date=current_date)
        
        # Логика распределения смен по дням для 1-й смены
        shift_schedule.shift_1_brigade_1 = shifts_1[(shifts_1.index(shift_1_brigade_1) + day) % 4]
        shift_schedule.shift_1_brigade_2 = shifts_1[(shifts_1.index(shift_1_brigade_2) + day) % 4]

        # Логика распределения смен по дням для 2-й смены
        shift_schedule.shift_2_brigade_1 = shifts_2[(shifts_2.index(shift_2_brigade_1) + day) % 4]
        shift_schedule.shift_2_brigade_2 = shifts_2[(shifts_2.index(shift_2_brigade_2) + day) % 4]
        shift_schedule.shift_2_brigade_3 = shifts_2[(shifts_2.index(shift_2_brigade_3) + day) % 4]
        shift_schedule.shift_2_brigade_4 = shifts_2[(shifts_2.index(shift_2_brigade_4) + day) % 4]

        shift_schedule.save()
    
    print("Заполнение расписания завершено.")