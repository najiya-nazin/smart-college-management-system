from django.urls import path
from .views import (
    HostelCreateAPIView,
    HostelListAPIView,
    HostelDetailAPIView,
    HostelUpdateAPIView,
    HostelPatchAPIView,
    HostelDeleteAPIView,

    HostelRoomCreateAPIView,
    HostelRoomListAPIView,
    HostelRoomDetailAPIView,
    HostelRoomUpdateAPIView,
    HostelRoomPatchAPIView,
    HostelRoomDeleteAPIView,
)

urlpatterns = [


    path("hostel_create/", HostelCreateAPIView.as_view(), name="hostel-create"),
    path("hostel_list/", HostelListAPIView.as_view(), name="hostel-list"),
    path("hostel_detail/<int:pk>/", HostelDetailAPIView.as_view(), name="hostel-detail"),
    path("hostel_update/<int:pk>/", HostelUpdateAPIView.as_view(), name="hostel-update"),
    path("hostel_patch/<int:pk>/", HostelPatchAPIView.as_view(), name="hostel-patch"),
    path("hostel_delete/<int:pk>/", HostelDeleteAPIView.as_view(), name="hostel-delete"),


    path("hostel_room_create/", HostelRoomCreateAPIView.as_view(), name="hostel-room-create"),
    path("hostel_room_list/", HostelRoomListAPIView.as_view(), name="hostel-room-list"),
    path("hostel_room_detail/<int:pk>/", HostelRoomDetailAPIView.as_view(), name="hostel-room-detail"),
    path("hostel_room_update/<int:pk>/", HostelRoomUpdateAPIView.as_view(), name="hostel-room-update"),
    path("hostel_room_patch/<int:pk>/", HostelRoomPatchAPIView.as_view(), name="hostel-room-patch"),
    path("hostel_room_delete/<int:pk>/", HostelRoomDeleteAPIView.as_view(), name="hostel-room-delete"),
]