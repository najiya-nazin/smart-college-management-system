from django import forms
from .models import Course


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = [
            "name",
            "code",
            "department",
            "duration",
            "description",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Course Name",
                "required": True,
                "minlength": 3,
            }),

            "code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Example: CSE101",
                "required": True,
                "minlength": 2,
                "maxlength": 10,
            }),

            "department": forms.Select(attrs={
                "class": "form-select",
                "required": True,
            }),

            "duration": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Duration",
                "required": True,
                "min": 1,
                "max": 10,
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Enter Course Description",
                "required": True,
                "minlength": 10,
            }),
        }

    # ---------------- Name Validation ----------------

    def clean_name(self):
        name = self.cleaned_data.get("name")

        if len(name.strip()) < 3:
            raise forms.ValidationError(
                "Course name must contain at least 3 characters."
            )

        if any(char.isdigit() for char in name):
            raise forms.ValidationError(
                "Course name cannot contain numbers."
            )

        return name

    # ---------------- Code Validation ----------------

    def clean_code(self):
        code = self.cleaned_data.get("code")

        if len(code.strip()) < 2:
            raise forms.ValidationError(
                "Course code must contain at least 2 characters."
            )

        return code

    # ---------------- Department Validation ----------------

    def clean_department(self):
        department = self.cleaned_data.get("department")

        if not department:
            raise forms.ValidationError(
                "Please select a department."
            )

        return department

    # ---------------- Duration Validation ----------------

    def clean_duration(self):
        duration = int(self.cleaned_data.get("duration"))

        if duration <= 0:
            raise forms.ValidationError(
            "Duration must be greater than 0."
            )

        return duration

    # ---------------- Description Validation ----------------

    def clean_description(self):
        description = self.cleaned_data.get("description")

        if len(description.strip()) < 10:
            raise forms.ValidationError(
                "Description must contain at least 10 characters."
            )

        return description