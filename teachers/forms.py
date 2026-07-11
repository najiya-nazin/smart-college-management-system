from django import forms
from .models import Teacher
from accounts.models import User


class TeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = [
            "user",
            "department",
            "qualification",
            "experience",
            "salary",
        ]

        widgets = {
            "user": forms.Select(attrs={
                "class": "form-select"
            }),

            "department": forms.Select(attrs={
                "class": "form-select"
            }),

            "qualification": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Qualification"
            }),

            "experience": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Years of Experience"
            }),

            "salary": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Salary"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["user"].queryset = User.objects.filter(role="TEACHER")