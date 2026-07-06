from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Exam
from .serializers import ExamSerializer


# Create Exam
class ExamCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ExamSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Exam created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# List All Exams
class ExamListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        exams = Exam.objects.all()
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data)


# Get Single Exam
class ExamDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            exam = Exam.objects.get(id=pk)
        except Exam.DoesNotExist:
            return Response(
                {"message": "Exam not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ExamSerializer(exam)
        return Response(serializer.data)


# Update Exam
class ExamUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            exam = Exam.objects.get(id=pk)
        except Exam.DoesNotExist:
            return Response(
                {"message": "Exam not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ExamSerializer(exam, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Exam updated successfully",
                    "data": serializer.data
                }
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Partial Update Exam
class ExamPatchAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            exam = Exam.objects.get(id=pk)
        except Exam.DoesNotExist:
            return Response(
                {"message": "Exam not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ExamSerializer(
            exam,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Exam updated successfully",
                    "data": serializer.data
                }
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete Exam
class ExamDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            exam = Exam.objects.get(id=pk)
        except Exam.DoesNotExist:
            return Response(
                {"message": "Exam not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        exam.delete()
        return Response(
            {"message": "Exam deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )