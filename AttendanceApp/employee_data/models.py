from django.db import models

class ShiftSchedule(models.Model):
    date = models.DateField()
    shift_1_brigade_1 = models.CharField(max_length=255, blank=True, null=True)
    shift_1_brigade_2 = models.CharField(max_length=255, blank=True, null=True)
    shift_2_brigade_1 = models.CharField(max_length=255, blank=True, null=True)
    shift_2_brigade_2 = models.CharField(max_length=255, blank=True, null=True)
    shift_2_brigade_3 = models.CharField(max_length=255, blank=True, null=True)
    shift_2_brigade_4 = models.CharField(max_length=255, blank=True, null=True)
    shift_3 = models.CharField(max_length=255, blank=True, null=True)
    shift_5_brigade_1 = models.CharField(max_length=255, blank=True, null=True)
    shift_5_brigade_2 = models.CharField(max_length=255, blank=True, null=True)
    shift_6 = models.CharField(max_length=255, blank=True, null=True)
    shift_7 = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.shift_1_brigade_1} - {self.shift_1_brigade_2} - {self.shift_2_brigade_1} - {self.shift_2_brigade_2} - {self.shift_2_brigade_3} - {self.shift_2_brigade_4} - {self.shift_3} - {self.shift_5_brigade_1} - {self.shift_5_brigade_2} - {self.shift_6} - {self.shift_7}"