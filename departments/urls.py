from django.urls import path
from .views import (
    DepartmentListCreateAPIView,
    DepartmentDetailAPIView
)

urlpatterns = [

    path(
        "",
        DepartmentListCreateAPIView.as_view(),
        name="department-list-create"
    ),

    path(
        "<int:pk>/",
        DepartmentDetailAPIView.as_view(),
        name="department-detail"
    ),

]