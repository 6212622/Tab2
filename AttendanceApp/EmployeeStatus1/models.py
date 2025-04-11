from django.db import models, connection

class Employee(models.Model):
    OwnerName = models.CharField(max_length=255)
    ProcessedCodeP = models.CharField(max_length=255)
    tabnumber = models.CharField(max_length=255)

    class Meta:
        db_table = 'tabel.dbo.tabbnumber'

    @staticmethod
    def find_by_last_four_digits(last_four_digits):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tabel.dbo.tabbnumber WHERE ProcessedCodeP = %s", [last_four_digits])
            rows = cursor.fetchall()
            for index, row in enumerate(rows):
                print(f"Строка {index}: {row}")
            return rows

    @staticmethod
    def find_by_tabnumber(tabnumber):
        with connection.cursor() as cursor:
            cursor.execute("SELECT TOP 1 CONCAT(name, ' ', girstname, ' ', midname) AS fio, tabnumber FROM OrionTMZ.dbo.LIST_users WHERE tabnumber = %s", [tabnumber])
            row = cursor.fetchone()
            if row:
                return {'fio': row[0], 'tabnumber': row[1]}  # Возвращаем словарь
            return None  # Если данных нет, возвращаем None

class Report(models.Model):
    tabnumber = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    shift = models.CharField(max_length=1)
    brigade = models.CharField(max_length=1)
    date = models.DateField()
    status = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.tabnumber} - {self.owner_name} - {self.date}"

    def set_default_brigade(self):
        if self.brigade is None:
            self.brigade = '0'  # Устанавливаем значение по умолчанию

class Smeny1C(models.Model):
    id = models.AutoField(primary_key=True)
    tabnumber = models.CharField(max_length=255)  # Замените на реальные поля таблицы
    smena = models.CharField(max_length=255)  # Замените на реальные поля таблицы

    class Meta:
        managed = False  # Django не будет управлять этой таблицей
        db_table = 'smeny1c'
        app_label = 'employee_data'