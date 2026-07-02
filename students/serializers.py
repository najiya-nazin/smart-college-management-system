from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):

    name = serializers.ReadOnlyField(source="user.name")
    email = serializers.ReadOnlyField(source="user.email")
    phone = serializers.ReadOnlyField(source="user.phone")

    department_name = serializers.ReadOnlyField(source="department.name")
    course_name = serializers.ReadOnlyField(source="course.name")

    class Meta:
        model = Student
        fields = [
            "id",
            "user",
            "student_id",
            "name",
            "email",
            "phone",
            "dob",
            "gender",
            "address",
            "department",
            "department_name",
            "course",
            "course_name",
            "semester",
            "admission_date",
            "guardian_name",
            "guardian_phone",
            "created_at",
            "updated_at",
        ]