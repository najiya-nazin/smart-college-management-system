from django import forms
from .models import Student
from accounts.models import User


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

        widgets = {

            "user": forms.Select(attrs={
                "class": "form-select"
            }),

            "student_id": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Student ID"
            }),

            "dob": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "gender": forms.Select(attrs={
                "class": "form-select"
            }),

            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Enter Address"
            }),

            "department": forms.Select(attrs={
                "class": "form-select"
            }),

            "course": forms.Select(attrs={
                "class": "form-select"
            }),

            "semester": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Semester"
            }),

            "admission_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "guardian_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Guardian Name"
            }),

            "guardian_phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Guardian Phone"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["user"].queryset = User.objects.filter(role="STUDENT").order_by("name")
    
        self.fields["user"].label_from_instance = lambda obj: f"{obj.name} ({obj.email})"


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "address",
            "guardian_name",
            "guardian_phone",
        ]

        widgets = {

                "address": forms.Textarea(attrs={
                    "class": "form-control",
                    "rows": 4,
                }),

                "guardian_name": forms.TextInput(attrs={
                    "class": "form-control",
                }),

                "guardian_phone": forms.TextInput(attrs={
                    "class": "form-control",
                }),

        }

        def clean_guardian_phone(self):
            phone = self.cleaned_data["guardian_phone"]

            if len(phone) != 10 or not phone.isdigit():
                raise forms.ValidationError(
                    "Guardian phone must contain exactly 10 digits."
                )

            return phone


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
                "phone",
        ]

        widgets = {

                "phone": forms.TextInput(attrs={
                    "class": "form-control",
                }),
        }

        def clean_phone(self):
            phone = self.cleaned_data["phone"]

            if len(phone) != 10 or not phone.isdigit():
                raise forms.ValidationError(
                    "Phone number must contain exactly 10 digits."
                )

            return phone
