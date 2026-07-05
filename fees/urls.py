from django.urls import path
from .views import (
    FeeListCreateAPIView,
    FeeDetailAPIView,
)

urlpatterns = [

    path(
        "",
        FeeListCreateAPIView.as_view(),
        name="fee-list-create"
    ),

    path(
        "<int:pk>/",
        FeeDetailAPIView.as_view(),
        name="fee-detail"
    ),

]
