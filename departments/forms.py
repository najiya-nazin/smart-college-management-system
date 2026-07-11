from django import forms
from .models import Department


class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ["name", "code", "description"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Department Name",
                "required": True,
            }),

            "code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Example: CSE, ECE, ME",
                "required": True,
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Enter Department Description",
                "required": True,
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()

        if len(name) < 3:
            raise forms.ValidationError(
                "Department name must contain at least 3 characters."
            )

        department = Department.objects.filter(name__iexact=name)

        if self.instance.pk:
            department = department.exclude(pk=self.instance.pk)

        if department.exists():
            raise forms.ValidationError(
                "Department already exists."
            )

        return name

    def clean_code(self):
        code = self.cleaned_data.get("code", "").strip().upper()

        if len(code) < 2:
            raise forms.ValidationError(
                "Department code must contain at least 2 characters."
            )

        department = Department.objects.filter(code__iexact=code)

        if self.instance.pk:
            department = department.exclude(pk=self.instance.pk)

        if department.exists():
            raise forms.ValidationError(
                "Department code already exists."
            )

        return code

    def clean_description(self):
        description = self.cleaned_data.get("description", "").strip()

        if len(description) < 10:
            raise forms.ValidationError(
                "Description must contain at least 10 characters."
            )

        return description

    