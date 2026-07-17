from django import forms
from .models import Teacher
from accounts.models import User
from departments.models import Department


class TeacherCreateForm(forms.ModelForm):

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Teacher Name"
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
        model = Teacher
        fields = [
            "name",
            "email",
            "phone",
            "password",
            "confirm_password",
            "department",
            "qualification",
            "experience",
            "salary",
        ]

        widgets = {
            "department": forms.Select(attrs={
                "class": "form-select",
            }),

            "qualification": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Qualification"
            }),

            "experience": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Years of Experience"
            }),

            "salary": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Salary"
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        if password != confirm:
            self.add_error(
                "confirm_password",
                "Passwords do not match."
            )

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "A user with this email already exists."
            )

        return email

class TeacherUpdateForm(forms.ModelForm):

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Teacher Name"
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
        model = Teacher
        fields = [
            "name",
            "email",
            "phone",
            "department",
            "qualification",
            "experience",
            "salary",
        ]

        widgets = {
            "department": forms.Select(attrs={
                "class": "form-select",
            }),

            "qualification": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Qualification"
            }),

            "experience": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Years of Experience"
            }),

            "salary": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Salary"
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
                "A user with this email already exists."
            )

        return email

    def save(self, commit=True):
        teacher = super().save(commit=False)

        teacher.user.name = self.cleaned_data["name"]
        teacher.user.email = self.cleaned_data["email"]
        teacher.user.phone = self.cleaned_data["phone"]

        if commit:
            teacher.user.save()
            teacher.save()

        return teacher
    

    
class TeacherProfileForm(forms.ModelForm):

    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Teacher
        fields = []   # Teacher model-ൽ നിന്ന് ഒരു field-ും edit ചെയ്യുന്നില്ല

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].initial = self.instance.user.name
        self.fields["email"].initial = self.instance.user.email

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exclude(
            pk=self.instance.user.pk
        ).exists():
            raise forms.ValidationError("Email already exists.")

        return email

    def save(self, commit=True):
        teacher = self.instance

        teacher.user.name = self.cleaned_data["name"]
        teacher.user.email = self.cleaned_data["email"]

        if commit:
            teacher.user.save()

        return teacher