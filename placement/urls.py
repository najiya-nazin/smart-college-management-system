from django.urls import path
from .views import (
    CompanyListCreateAPIView,
    CompanyDetailAPIView,
    PlacementListCreateAPIView,
    PlacementDetailAPIView,
)

urlpatterns = [

    path(
        "company/",
        CompanyListCreateAPIView.as_view(),
        name="company-list-create"
    ),

    path(
        "company/<int:pk>/",
        CompanyDetailAPIView.as_view(),
        name="company-detail"
    ),

    path(
        "",
        PlacementListCreateAPIView.as_view(),
        name="placement-list-create"
    ),

    path(
        "<int:pk>/",
        PlacementDetailAPIView.as_view(),
        name="placement-detail"
    ),
]