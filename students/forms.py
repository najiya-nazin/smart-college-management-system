from django import forms
from .models import Student


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = [
            "user",
            "student_id",
            "dob",
            "gender",
            "address",
            "department",
            "course",
            "semester",
            "admission_date",
            "guardian_name",
            "guardian_phone",
        ]