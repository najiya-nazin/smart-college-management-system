from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Student
from .serializers import StudentSerializer


class StudentListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        students = Student.objects.select_related(
            "user",
            "department",
            "course"
        ).all().order_by("student_id")

        serializer = StudentSerializer(
            students,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):

        serializer = StudentSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class StudentDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        return get_object_or_404(
            Student.objects.select_related(
                "user",
                "department",
                "course"
            ),
            pk=pk
        )

    def get(self, request, pk):

        student = self.get_object(pk)

        serializer = StudentSerializer(student)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):

        student = self.get_object(pk)

        serializer = StudentSerializer(
            student,
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def patch(self, request, pk):

        student = self.get_object(pk)

        serializer = StudentSerializer(
            student,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):

        student = self.get_object(pk)

        student.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
