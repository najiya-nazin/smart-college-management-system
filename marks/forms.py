from django import forms
from .models import Marks


class MarksForm(forms.ModelForm):

    class Meta:
        model = Marks
        fields = [
            "student",
            "course",
            "marks_obtained",
            "max_marks",
            "grade",
        ]

        widgets = {
            "student": forms.Select(attrs={
                "class": "form-select"
            }),
            "course": forms.Select(attrs={
                "class": "form-select"
            }),
            "marks_obtained": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Marks Obtained"
            }),
            "max_marks": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Maximum Marks"
            }),
            "grade": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Example: A+, A, B+, B"
            }),
        }