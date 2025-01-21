from django.db import models

class EmployeeData(models.Model):
    tabnumber = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    # Добавьте другие поля здесь
