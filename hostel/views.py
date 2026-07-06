from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Hostel, HostelRoom
from .serializers import HostelSerializer, HostelRoomSerializer


class HostelCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = HostelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HostelListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        hostels = Hostel.objects.all()
        serializer = HostelSerializer(hostels, many=True)
        return Response(serializer.data)


class HostelDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            hostel = Hostel.objects.get(id=pk)
        except Hostel.DoesNotExist:
            return Response({"message": "Hostel not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = HostelSerializer(hostel)
        return Response(serializer.data)


class HostelUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            hostel = Hostel.objects.get(id=pk)
        except Hostel.DoesNotExist:
            return Response({"message": "Hostel not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = HostelSerializer(hostel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HostelPatchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            hostel = Hostel.objects.get(id=pk)
        except Hostel.DoesNotExist:
            return Response({"message": "Hostel not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = HostelSerializer(hostel, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HostelDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            hostel = Hostel.objects.get(id=pk)
        except Hostel.DoesNotExist:
            return Response({"message": "Hostel not found"}, status=status.HTTP_404_NOT_FOUND)

        hostel.delete()
        return Response({"message": "Hostel deleted successfully"}, status=status.HTTP_204_NO_CONTENT)




class HostelRoomCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = HostelRoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HostelRoomListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rooms = HostelRoom.objects.all()
        serializer = HostelRoomSerializer(rooms, many=True)
        return Response(serializer.data)


class HostelRoomDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            room = HostelRoom.objects.get(id=pk)
        except HostelRoom.DoesNotExist:
            return Response({"message": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = HostelRoomSerializer(room)
        return Response(serializer.data)


class HostelRoomUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            room = HostelRoom.objects.get(id=pk)
        except HostelRoom.DoesNotExist:
            return Response({"message": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = HostelRoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HostelRoomPatchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            room = HostelRoom.objects.get(id=pk)
        except HostelRoom.DoesNotExist:
            return Response({"message": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = HostelRoomSerializer(room, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HostelRoomDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            room = HostelRoom.objects.get(id=pk)
        except HostelRoom.DoesNotExist:
            return Response({"message": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

        room.delete()
        return Response({"message": "Room deleted successfully"}, status=status.HTTP_204_NO_CONTENT)