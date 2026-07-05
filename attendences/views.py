from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Attendance
from .serializers import AttendanceSerializer


class AttendanceListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        attendance = Attendance.objects.select_related(
            "student"
        ).all().order_by("-date")

        serializer = AttendanceSerializer(attendance, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        serializer = AttendanceSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AttendanceDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        return get_object_or_404(
            Attendance.objects.select_related("student"),
            pk=pk
        )

    def get(self, request, pk):

        attendance = self.get_object(pk)

        serializer = AttendanceSerializer(attendance)

        return Response(serializer.data)

    def put(self, request, pk):

        attendance = self.get_object(pk)

        serializer = AttendanceSerializer(attendance, data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)

    def patch(self, request, pk):

        attendance = self.get_object(pk)

        serializer = AttendanceSerializer(
            attendance,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):

        attendance = self.get_object(pk)

        attendance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)