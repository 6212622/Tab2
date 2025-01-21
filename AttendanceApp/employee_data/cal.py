from datetime import datetime
from collections import defaultdict
from calendar import monthrange

def calculate_work_time_for_month(tabnumber, month, year):
    print(f"Функция вызвана с параметрами в внутри calculate_work_time_for_month: tabnumber={tabnumber}, month={month}, year={year}")
    
    total_days = monthrange(year, month)[1]
    days = list(range(1, total_days + 1))  # Список дней месяца
    times = []
  
    print(f"значения total_days: {total_days}")

    # Подключение к базе данных
    from django.db import connection
    
    # Запрос данных из базы
    query = f"""
    WITH Aa AS (
      SELECT 
        for1c.*, 
        DENSE_RANK() OVER(PARTITION BY tabnumber ORDER BY timeval) AS a,  
        DATEDIFF(MINUTE, timeval, LEAD(timeval) OVER(PARTITION BY tabnumber ORDER BY timeval)) AS zb, 
        CAST(TimeVal AS DATE) AS data
      FROM [OrionTMZ].[dbo].[FOR1C]
      WHERE tabnumber = {tabnumber}
        AND MONTH(timeval) = {month}
        AND YEAR(timeval) = {year}
    )
    SELECT 
      CAST(data AS DATE) AS day,
      SUM(zb) / 60 AS hours,
      SUM(zb) % 60 AS minutes
    FROM Aa
    WHERE ZoneIndex = 'ВХОД'
    GROUP BY CAST(data AS DATE)
    ORDER BY day;
    """
    print("Запрос сформирован:")
    print(query)

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        print("Данные получены из базы данных:")
        for i in rows:
            print(f"В внутри функции calculate_work_time_for_month - обращения к базе: {i}")
    # Формирование результата
    report_data = {
        "days": [],
        "times": [],
    }
    
    for row in rows:
      print(f"Обработка строки: {row}")
      day, hours, minutes = row
      if hours is None:
          hours = 0
      if minutes is None:
          minutes = 0
      report_data["days"].append(day.day)  # Добавляем только число дня
      report_data["times"].append(f"{int(hours)}ч.{int(minutes)}м.")
    
    non_empty_days = []
    empty_days = []
 
    for day in days:
      # Пример проверки данных (замените на реальную логику)
      if day in report_data["days"]:
          index = report_data["days"].index(day)
          times.append(report_data["times"][index])
          non_empty_days.append(day)
      else:
          times.append("0")  # Если данных нет, заполняем нулем
          empty_days.append(day)

    print(f"В внутри функции calculate_work_time_for_month: {report_data}")
    print(f"Непустые дни: {non_empty_days}")
    print(f"Пустые дни: {empty_days}")
    return report_data, non_empty_days, empty_days