from django import forms
from .models import Marks


class MarksForm(forms.ModelForm):

    class Meta:
        model = Marks
        fields = [
            "student",
            "course",
            "marks_obtained",
            "max_marks",
        ]

        widgets = {
            "student": forms.Select(attrs={
                "class": "form-select"
            }),
            "course": forms.Select(attrs={
                "class": "form-select"
            }),
            "marks_obtained": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Marks Obtained"
            }),
            "max_marks": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Maximum Marks"
            }),
            "grade": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Example: A+, A, B+, B"
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        obtained = cleaned_data.get("marks_obtained")
        maximum = cleaned_data.get("max_marks")

        if obtained is not None and maximum is not None:

            if maximum <= 0:
                self.add_error(
                    "max_marks",
                    "Maximum marks must be greater than zero."
                )

            elif obtained > maximum:
                self.add_error(
                    "marks_obtained",
                    "Marks obtained cannot be greater than maximum marks."
                )

        return cleaned_data

    def save(self, commit=True):

        marks = super().save(commit=False)

        percentage = (
                             marks.marks_obtained / marks.max_marks
                     ) * 100

        if percentage >= 90:
            marks.grade = "A+"

        elif percentage >= 80:
            marks.grade = "A"

        elif percentage >= 70:
            marks.grade = "B+"

        elif percentage >= 60:
            marks.grade = "B"

        elif percentage >= 50:
            marks.grade = "C"

        elif percentage >= 40:
            marks.grade = "D"

        else:
            marks.grade = "F"

        if commit:
            marks.save()

        return marks
