from django import forms
from .models import Company, Placement


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = [
            "name",
            "location",
            "website",
            "email",
            "phone",
        ]



        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Company Name"
            }),
            "location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Location"
            }),
            "website": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "https://example.com"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "company@example.com"
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Phone Number"
            }),
        }


class PlacementForm(forms.ModelForm):

    class Meta:
        model = Placement
        fields = [
            "student",
            "company",
            "job_role",
            "package",
            "placement_date",
            "status",
            "remarks",
        ]


        widgets = {
            "student": forms.Select(attrs={
                "class": "form-select"
            }),
            "company": forms.Select(attrs={
                "class": "form-select"
            }),
            "job_role": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Job Role"
            }),
            "package": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Package"
            }),
            "placement_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "status": forms.Select(attrs={
                "class": "form-select"
            }),
            "remarks": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Enter Remarks"
            }),
        }