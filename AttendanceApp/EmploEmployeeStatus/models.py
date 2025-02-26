from django.db import models

class Employee(models.Model):
    OwnerName = models.CharField(max_length=255)
    ProcessedCodeP = models.CharField(max_length=255)
    tabnumber = models.CharField(max_length=255)

    class Meta:
        db_table = 'tabel.dbo.tabbnumber'