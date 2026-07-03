from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Marks
from .serializers import MarksSerializer



class AddMarks(APIView):

    def post(self, request):
        serializer = MarksSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Marks Added Successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MarksList(APIView):

    def get(self, request):
        marks = Marks.objects.all()
        serializer = MarksSerializer(marks, many=True)

        return Response(
            {
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )



class MarksDetail(APIView):

    def get(self, request, pk):
        try:
            marks = Marks.objects.get(pk=pk)
        except Marks.DoesNotExist:
            return Response(
                {"message": "Marks Not Found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MarksSerializer(marks)
        return Response(serializer.data, status=status.HTTP_200_OK)



class EditMarks(APIView):

    def put(self, request, pk):
        try:
            marks = Marks.objects.get(pk=pk)
        except Marks.DoesNotExist:
            return Response(
                {"message": "Marks Not Found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MarksSerializer(marks, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Marks Updated Successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            marks = Marks.objects.get(pk=pk)
        except Marks.DoesNotExist:
            return Response(
                {"message": "Marks Not Found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MarksSerializer(
            marks,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Marks Partially Updated Successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DeleteMarks(APIView):

    def delete(self, request, pk):
        try:
            marks = Marks.objects.get(pk=pk)
        except Marks.DoesNotExist:
            return Response(
                {"message": "Marks Not Found"},
                status=status.HTTP_404_NOT_FOUND
            )

        marks.delete()

        return Response(
            {
                "message": "Marks Deleted Successfully"
            },
            status=status.HTTP_200_OK
        )