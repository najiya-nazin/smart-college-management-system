from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Timetable
from .serializers import TimetableSerializer
from rest_framework.permissions import IsAuthenticated


# Create Timetable
class CreateTimetable(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TimetableSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Timetable Created Successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# View All Timetables
class TimetableList(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        timetable = Timetable.objects.all()
        serializer = TimetableSerializer(
            timetable,
            many=True
        )

        return Response(
            {
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# View Single Timetable
class TimetableDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        try:
            timetable = Timetable.objects.get(pk=pk)

        except Timetable.DoesNotExist:

            return Response(
                {
                    "message": "Timetable Not Found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TimetableSerializer(timetable)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


# Update Timetable
class UpdateTimetable(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        try:
            timetable = Timetable.objects.get(pk=pk)

        except Timetable.DoesNotExist:

            return Response(
                {
                    "message": "Timetable Not Found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TimetableSerializer(
            timetable,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "Timetable Updated Successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):

        permission_classes = [IsAuthenticated]

        try:
            timetable = Timetable.objects.get(pk=pk)

        except Timetable.DoesNotExist:

            return Response(
                {
                    "message": "Timetable Not Found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TimetableSerializer(
            timetable,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "Timetable Partially Updated Successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# Delete Timetable
class DeleteTimetable(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        try:
            timetable = Timetable.objects.get(pk=pk)

        except Timetable.DoesNotExist:

            return Response(
                {
                    "message": "Timetable Not Found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        timetable.delete()

        return Response(
            {
                "message": "Timetable Deleted Successfully"
            },
            status=status.HTTP_200_OK
        )