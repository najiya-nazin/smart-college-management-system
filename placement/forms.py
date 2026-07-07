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