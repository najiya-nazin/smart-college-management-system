from rest_framework import serializers
from .models import Marks


class MarksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Marks
        fields = [
            'id',
            'student',
            'course',
            'marks_obtained',
            'max_marks',
            'grade',
        ]

        extra_kwargs = {
            'student': {'required': True},
            'course': {'required': True},
            'marks_obtained': {'required': True},
            'max_marks': {'required': True},
            'grade': {'required': True},
        }