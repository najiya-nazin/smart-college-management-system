from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Company, Placement
from .serializers import CompanySerializer, PlacementSerializer


class CompanyListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        companies = Company.objects.all().order_by("name")

        serializer = CompanySerializer(
            companies,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):

        serializer = CompanySerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class CompanyDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        return get_object_or_404(
            Company,
            pk=pk
        )

    def get(self, request, pk):

        company = self.get_object(pk)

        serializer = CompanySerializer(company)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):

        company = self.get_object(pk)

        serializer = CompanySerializer(
            company,
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def patch(self, request, pk):

        company = self.get_object(pk)

        serializer = CompanySerializer(
            company,
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

        company = self.get_object(pk)

        company.delete()

        return Response(
            {
                "message": "Company deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )


class PlacementListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        placements = Placement.objects.select_related(
            "student",
            "student__user",
            "company"
        ).all().order_by("-placement_date")

        serializer = PlacementSerializer(
            placements,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):

        serializer = PlacementSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class PlacementDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        return get_object_or_404(
            Placement.objects.select_related(
                "student",
                "student__user",
                "company"
            ),
            pk=pk
        )

    def get(self, request, pk):

        placement = self.get_object(pk)

        serializer = PlacementSerializer(placement)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):

        placement = self.get_object(pk)

        serializer = PlacementSerializer(
            placement,
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def patch(self, request, pk):

        placement = self.get_object(pk)

        serializer = PlacementSerializer(
            placement,
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

        placement = self.get_object(pk)

        placement.delete()

        return Response(
            {
                "message": "Placement record deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )