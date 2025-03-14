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
            return rows

class Report(models.Model):
    tabnumber = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    shift = models.CharField(max_length=1)
    brigade = models.CharField(max_length=1)
    date = models.DateField()
    status = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.tabnumber} - {self.owner_name} - {self.date}"