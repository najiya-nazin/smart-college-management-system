from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Teacher
from .serializers import TeacherSerializer



class AddTeacher(APIView):

    def post(self, request):
        serializer = TeacherSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Teacher Added Successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TeacherList(APIView):

    def get(self, request):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)

        return Response(
            {
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


class TeacherDetail(APIView):

    def get(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response(
                {
                    "message": "Teacher Not Found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TeacherSerializer(teacher)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )



class EditTeacher(APIView):

    def put(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response(
                {"message": "Teacher Not Found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TeacherSerializer(teacher, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Teacher Updated Successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response(
                {"message": "Teacher Not Found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TeacherSerializer(
            teacher,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Teacher Partially Updated Successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DeleteTeacher(APIView):

    def delete(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response(
                {
                    "message": "Teacher Not Found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        teacher.delete()

        return Response(
            {
                "message": "Teacher Deleted Successfully"
            },
            status=status.HTTP_200_OK
        )