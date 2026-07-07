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