from django import forms
from .models import Exam


class ExamForm(forms.ModelForm):

    class Meta:
        model = Exam
        fields = [
            "name",
            "course",
            "exam_date",
            "total_marks",
        ]


        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Exam Name"
            }),

            "course": forms.Select(attrs={
                "class": "form-select"
            }),

            "exam_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "total_marks": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Total Marks"
            }),
        }