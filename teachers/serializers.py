from rest_framework import serializers
from .models import Teacher


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = [
            'id',
            'user',
            'name',
            'department',
            'email',
            'phone',
            'qualification',
            'experience',
            'salary',
        ]

        extra_kwargs = {
            'name': {'required': True},
            'department': {'required': True},
            'email': {'required': True},
            'phone': {'required': True},
            'qualification': {'required': True},
            'experience': {'required': True},
            'salary': {'required': True},
        }