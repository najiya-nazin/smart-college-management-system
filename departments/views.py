from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Department
from .serializers import DepartmentSerializer


class DepartmentListCreateAPIView(APIView):

    # permission_classes = [IsAuthenticated]

    def get(self, request):

        departments = Department.objects.all().order_by("name")

        serializer = DepartmentSerializer(
            departments,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):

        serializer = DepartmentSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class DepartmentDetailAPIView(APIView):

    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        return get_object_or_404(
            Department,
            pk=pk
        )

    def get(self, request, pk):

        department = self.get_object(pk)

        serializer = DepartmentSerializer(
            department
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):

        department = self.get_object(pk)

        serializer = DepartmentSerializer(
            department,
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def patch(self, request, pk):

        department = self.get_object(pk)

        serializer = DepartmentSerializer(
            department,
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

        department = self.get_object(pk)

        department.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )