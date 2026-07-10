from django import forms
from .models import Timetable


class TimetableForm(forms.ModelForm):

    class Meta:
        model = Timetable
        fields = [
            "course",
            "teacher",
            "class_name",
            "room_no",
            "day",
            "start_time",
            "end_time",
        ]

        widgets = {
            "course": forms.Select(attrs={
                "class": "form-select",
                "required": True,
            }),

            "teacher": forms.Select(attrs={
                "class": "form-select",
                "required": True,
            }),

            "class_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Class Name",
                "required": True,
                "minlength": 2,
            }),

            "room_no": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Room Number",
                "required": True,
                "minlength": 2,
            }),

            "day": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Monday",
                "required": True,
            }),

            "start_time": forms.TimeInput(attrs={
                "class": "form-control",
                "type": "time",
                "required": True,
            }),

            "end_time": forms.TimeInput(attrs={
                "class": "form-control",
                "type": "time",
                "required": True,
            }),
        }

    def clean_class_name(self):
        class_name = self.cleaned_data.get("class_name")

        if len(class_name.strip()) < 2:
            raise forms.ValidationError(
                "Class name must contain at least 2 characters."
            )

        return class_name

    def clean_room_no(self):
        room_no = self.cleaned_data.get("room_no")

        if len(room_no.strip()) < 2:
            raise forms.ValidationError(
                "Room number must contain at least 2 characters."
            )

        return room_no

    def clean_day(self):
        day = self.cleaned_data.get("day").strip().capitalize()

        valid_days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        if day not in valid_days:
            raise forms.ValidationError(
                "Please enter a valid day."
            )

        return day

    def clean(self):
        cleaned_data = super().clean()

        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time and end_time <= start_time:
            self.add_error(
                "end_time",
                "End time must be later than start time."
            )

        return cleaned_data