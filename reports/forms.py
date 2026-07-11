from django import forms
from django.core.exceptions import ValidationError
from .models import Report


class ReportForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = [
            "report_type",
            "generated_by",
            "file",
        ]



        widgets = {
            "report_type": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Report Type"
            }),

            "generated_by": forms.Select(attrs={
                "class": "form-select"
            }),

            "file": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
        }

    def clean_report_type(self):
        report_type = self.cleaned_data.get("report_type")

        if not report_type.replace(" ", "").isalpha():
            raise ValidationError(
                "Report Type must contain only letters and spaces."
            )

        return report_type.title()
