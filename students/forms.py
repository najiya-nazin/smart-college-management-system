from django import forms
from .models import Student
from accounts.models import User


class StudentCreateForm(forms.ModelForm):

    # User Fields
    name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Student Name"
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Email Address"
        })
    )

    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Phone Number"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Create Password"
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirm Password"
        })
    )

    class Meta:
        model = Student

        fields = [
            "name",
            "email",
            "phone",
            "password",
            "confirm_password",

            "student_id",
            "dob",
            "gender",
            "address",

            "department",
            "semester",
            # "course",
            "admission_date",

            "guardian_name",
            "guardian_phone",
        ]

        widgets = {

            "student_id": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Student ID"
            }),

            "dob": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "gender": forms.Select(attrs={
                "class": "form-select",
                "placeholder": "Select Gender",
            }),

            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Address"
            }),

            "department": forms.Select(attrs={
                "class": "form-select"
            }),

            # "course": forms.SelectMultiple(attrs={
            #     "class": "form-select"
            # }),

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

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error(
                "confirm_password",
                "Passwords do not match."
            )

        return cleaned_data

    def clean_email(self):

        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Email already exists."
            )

        return email

    def clean_phone(self):

        phone = self.cleaned_data["phone"]

        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError(
                "Phone number must contain exactly 10 digits."
            )

        return phone

    def clean_guardian_phone(self):

        phone = self.cleaned_data["guardian_phone"]

        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError(
                "Guardian phone must contain exactly 10 digits."
            )

        return phone

    def save(self, commit=True):

        student = super().save(commit=False)

        user = User.objects.create_user(

            name=self.cleaned_data["name"],

            email=self.cleaned_data["email"],

            phone=self.cleaned_data["phone"],

            password=self.cleaned_data["password"],

            role="STUDENT",

        )

        student.user = user

        if commit:
            student.save()

            self.save_m2m()

        return student


class StudentUpdateForm(forms.ModelForm):

    # User Fields
    name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Student Name"
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Email Address"
        })
    )

    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Phone Number"
        })
    )

    class Meta:
        model = Student

        fields = [
            "name",
            "email",
            "phone",

            "student_id",
            "dob",
            "gender",
            "address",

            "department",
            # "course",
            "semester",
            "admission_date",

            "guardian_name",
            "guardian_phone",
        ]

        widgets = {

            "student_id": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "dob": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "gender": forms.Select(attrs={
                "class": "form-select",
                "placeholder": "Select Gender",
            }),

            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),

            "department": forms.Select(attrs={
                "class": "form-select"
            }),

            # "course": forms.SelectMultiple(attrs={
            #     "class": "form-select"
            # }),

            "semester": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "admission_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "guardian_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "guardian_phone": forms.TextInput(attrs={
                "class": "form-control"
            }),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:

            self.fields["name"].initial = self.instance.user.name
            self.fields["email"].initial = self.instance.user.email
            self.fields["phone"].initial = self.instance.user.phone

    def clean_email(self):

        email = self.cleaned_data["email"]

        qs = User.objects.filter(email=email).exclude(
            pk=self.instance.user.pk
        )

        if qs.exists():
            raise forms.ValidationError(
                "Email already exists."
            )

        return email

    def clean_phone(self):

        phone = self.cleaned_data["phone"]

        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError(
                "Phone number must contain exactly 10 digits."
            )

        return phone

    def clean_guardian_phone(self):

        phone = self.cleaned_data["guardian_phone"]

        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError(
                "Guardian phone must contain exactly 10 digits."
            )

        return phone

    def save(self, commit=True):

        student = super().save(commit=False)

        student.user.name = self.cleaned_data["name"]
        student.user.email = self.cleaned_data["email"]
        student.user.phone = self.cleaned_data["phone"]

        if commit:
            student.user.save()
            student.save()
            self.save_m2m()

        return student


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
                "placeholder": "Enter Guardian Name",
            }),

            "guardian_phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Guardian Phone",
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
                "placeholder": "Enter Phone Number",
            }),

        }

    def clean_phone(self):

        phone = self.cleaned_data["phone"]

        if len(phone) != 10 or not phone.isdigit():
            raise forms.ValidationError(
                "Phone number must contain exactly 10 digits."
            )

        return phone
