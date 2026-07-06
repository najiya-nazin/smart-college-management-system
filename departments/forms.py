from django import forms
from .models import Department


class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data.get("name")

        department = Department.objects.filter(name__iexact=name)

        if self.instance.pk:
            department = department.exclude(pk=self.instance.pk)

        if department.exists():
            raise forms.ValidationError(
                "Department already exists."
            )

        return name