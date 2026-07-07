from django import forms
from .models import Teacher


class TeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = [
            "user",
            "name",
            "department",
            "email",
            "phone",
            "qualification",
            "experience",
            "salary",
        ]