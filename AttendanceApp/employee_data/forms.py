from django import forms

class EmployeeReportForm(forms.Form):
    tabnumber = forms.IntegerField(label='Табельный номер')
    month = forms.CharField(label='Месяц', max_length=7, help_text='YYYY-MM')
