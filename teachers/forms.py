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
                "class": "form-select",
            }),

            "department": forms.Select(attrs={
                "class": "form-select",
            }),

            "qualification": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Qualification"
            }),

            "experience": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Years of Experience",
                "min": "0",
            }),

            "salary": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Salary",
                "min": "1",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].queryset = User.objects.filter(role="TEACHER")

    def clean_experience(self):
        experience = self.cleaned_data.get("experience")

        if experience is not None and experience < 0:
            raise forms.ValidationError(
                "Experience cannot be negative."
            )

        return experience

    def clean_salary(self):
        salary = self.cleaned_data.get("salary")

        if salary is not None and salary <= 0:
            raise forms.ValidationError(
                "Salary must be greater than zero."
            )

        return salary

    def clean_qualification(self):
        qualification = self.cleaned_data.get("qualification", "").strip()

        if len(qualification) < 3:
            raise forms.ValidationError(
                "Qualification must contain at least 3 characters."
            )

        return qualification