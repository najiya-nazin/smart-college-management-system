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

        def clean_job_role(self):
            job_role = self.cleaned_data.get("job_role")

            if len(job_role.strip()) < 3:
                raise forms.ValidationError(
                    "Job role must contain at least 3 characters."
                )

            return job_role.title()

        def clean_package(self):

            package = self.cleaned_data.get("package")

            if package <= 0:
                raise forms.ValidationError(
                    "Package must be greater than zero."
                )

            return package

        def clean(self):

            cleaned_data = super().clean()

            student = cleaned_data.get("student")
            company = cleaned_data.get("company")
            job_role = cleaned_data.get("job_role")

            if student and company and job_role:

                duplicate = Placement.objects.filter(

                    student=student,
                    company=company,
                    job_role__iexact=job_role

                )

                if self.instance.pk:
                    duplicate = duplicate.exclude(pk=self.instance.pk)

                if duplicate.exists():
                    raise forms.ValidationError(

                        "This student already has a placement record for this company and job role."

                    )

            return cleaned_data