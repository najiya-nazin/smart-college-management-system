from django.urls import path
from .views import (
    StudentListCreateAPIView,
    StudentDetailAPIView,
)

urlpatterns = [

    path(
        "",
        StudentListCreateAPIView.as_view(),
        name="student-list-create"
    ),

    path(
        "<int:pk>/",
        StudentDetailAPIView.as_view(),
        name="student-detail"
    ),

]
