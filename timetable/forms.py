from django import forms
from .models import Timetable


class TimetableForm(forms.ModelForm):

    CLASS_CHOICES = [
        ("BCom CA", "B.Com"),
        ("BCom Finance", "BCom Finance"),
        ("BCom Coperation", "BCom Coperation"),
        ("BCA", "BCA"),
        ("BSC Computer", "BSC Computer"),
        ("BSC Chemistry", "BSC Chemistry"),
        ("BSC Maths", "BSC Maths"),
        ("BA English", "BA English"),

    ]

    class_name = forms.ChoiceField(
        choices=CLASS_CHOICES,
        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )

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

        DAY_CHOICES = [
            ("Monday", "Monday"),
            ("Tuesday", "Tuesday"),
            ("Wednesday", "Wednesday"),
            ("Thursday", "Thursday"),
            ("Friday", "Friday"),
            ("Saturday", "Saturday"),
        ]

        widgets = {
            "course": forms.Select(attrs={
                "class": "form-select",
                "required": True,
                "id": "course-select",
            }),


            "teacher": forms.Select(attrs={
                "class": "form-select",
                "required": True,
                "id": "teacher-select",
            }),


            "room_no": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Room Number",
                "required": True,
                "minlength": 2,
            }),

            "day": forms.Select(
                choices=DAY_CHOICES,
                attrs={
                    "class": "form-select",
                    "required": True,
                }
            ),

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

    def clean_room_no(self):
        room_no = self.cleaned_data.get("room_no")

        if len(room_no.strip()) < 2:
            raise forms.ValidationError(
                "Room number must contain at least 2 characters."
            )

        return room_no

    # def clean_day(self):
    #     day = self.cleaned_data.get("day").strip().capitalize()
    #
    #     valid_days = [
    #         "Monday",
    #         "Tuesday",
    #         "Wednesday",
    #         "Thursday",
    #         "Friday",
    #         "Saturday",
    #         "Sunday",
    #     ]
    #
    #     if day not in valid_days:
    #         raise forms.ValidationError(
    #             "Please enter a valid day."
    #         )
    #
    #     return day

    def clean(self):

        cleaned_data = super().clean()

        course = cleaned_data.get("course")
        teacher = cleaned_data.get("teacher")
        class_name = cleaned_data.get("class_name")
        room_no = cleaned_data.get("room_no")
        day = cleaned_data.get("day")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        # End time validation
        if start_time and end_time and end_time <= start_time:
            self.add_error(
                "end_time",
                "End time must be later than start time."
            )

        # Teacher belongs to same department
        if course and teacher:
            if teacher.department != course.department:
                self.add_error(
                    "teacher",
                    "Selected teacher does not belong to this course's department."
                )

        # Teacher conflict
        if teacher and day and start_time and end_time:

            teacher_conflict = Timetable.objects.filter(
                teacher=teacher,
                day=day,
                start_time__lt=end_time,
                end_time__gt=start_time,
            )

            if self.instance.pk:
                teacher_conflict = teacher_conflict.exclude(pk=self.instance.pk)

            if teacher_conflict.exists():
                self.add_error(
                    "teacher",
                    "This teacher already has another class during this time."
                )

        # Room conflict
        if room_no and day and start_time and end_time:

            room_conflict = Timetable.objects.filter(
                room_no=room_no,
                day=day,
                start_time__lt=end_time,
                end_time__gt=start_time,
            )

            if self.instance.pk:
                room_conflict = room_conflict.exclude(pk=self.instance.pk)

            if room_conflict.exists():
                self.add_error(
                    "room_no",
                    "This room is already occupied during this time."
                )

        # Class conflict
        if class_name and day and start_time and end_time:

            class_conflict = Timetable.objects.filter(
                class_name=class_name,
                day=day,
                start_time__lt=end_time,
                end_time__gt=start_time,
            )

            if self.instance.pk:
                class_conflict = class_conflict.exclude(pk=self.instance.pk)

            if class_conflict.exists():
                self.add_error(
                    "class_name",
                    "This class already has another subject during this time."
                )

        return cleaned_data