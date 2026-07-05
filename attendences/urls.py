from django.urls import path
from .views import (
    AttendanceListCreateAPIView,
    AttendanceDetailAPIView,
)

urlpatterns = [

    path(
        "",
        AttendanceListCreateAPIView.as_view(),
        name="attendance-list-create"
    ),

    path(
        "<int:pk>/",
        AttendanceDetailAPIView.as_view(),
        name="attendance-detail"
    ),

]