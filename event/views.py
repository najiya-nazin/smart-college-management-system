from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Event
from .serializers import EventSerializer
from rest_framework.permissions import IsAuthenticated


# Create Event
class EventCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = EventSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# List All Events
class EventListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


# Get Single Event
class EventDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            event = Event.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response(
                {"message": "Event not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EventSerializer(event)
        return Response(serializer.data)


# Update Event
class EventUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            event = Event.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response(
                {"message": "Event not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EventSerializer(event, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete Event
class EventDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            event = Event.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response(
                {"message": "Event not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        event.delete()
        return Response(
            {"message": "Event deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


class EventPatchAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            event = Event.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response(
                {"message": "Event not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EventSerializer(
            event,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Event updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)