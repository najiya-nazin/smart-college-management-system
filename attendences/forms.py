from django import forms
from .models import Attendance


class AttendanceForm(forms.ModelForm):

    class Meta:
        model = Attendance
        fields = [
            "student",
            "date",
            "status",
        ]


        widgets = {

            "student": forms.Select(attrs={
                "class": "form-select form-select-lg"
            }),

            "date": forms.DateInput(attrs={
                "class": "form-control form-control-lg",
                "type": "date"
            }),

            "status": forms.Select(attrs={
                "class": "form-select form-select-lg"
            }),
        }