from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Fee
from .serializers import FeeSerializer


class FeeListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        fees = Fee.objects.select_related(
            "student",
            "student__user"
        ).all().order_by("-payment_date")

        serializer = FeeSerializer(
            fees,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):

        serializer = FeeSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class FeeDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        return get_object_or_404(
            Fee.objects.select_related(
                "student",
                "student__user"
            ),
            pk=pk
        )

    def get(self, request, pk):

        fee = self.get_object(pk)

        serializer = FeeSerializer(fee)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):

        fee = self.get_object(pk)

        serializer = FeeSerializer(
            fee,
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def patch(self, request, pk):

        fee = self.get_object(pk)

        serializer = FeeSerializer(
            fee,
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

        fee = self.get_object(pk)

        fee.delete()

        return Response(
            {
                "message": "Fee record deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )
