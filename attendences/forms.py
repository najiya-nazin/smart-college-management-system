from django import forms
from .models import Attendance
from django.utils import timezone


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


    def clean_date(self):
        date = self.cleaned_data["date"]

        if date < timezone.now().date():
            raise forms.ValidationError(
                "Past dates are not allowed."
            )

        return date    


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

     
        self.fields["date"].widget.attrs["min"] = timezone.now().date().isoformat()


        self.fields["student"].error_messages = {
            "required": ""
        }

        self.fields["date"].error_messages = {
            "required": ""
        }

        self.fields["status"].error_messages = {
            "required": ""
        }