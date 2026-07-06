from django.urls import path
from .views import (
    EventCreateAPIView,
    EventListAPIView,
    EventDetailAPIView,
    EventUpdateAPIView,
    EventDeleteAPIView,
    EventPatchAPIView,
)

urlpatterns = [
    path('event_create/', EventCreateAPIView.as_view(), name='event-create'),
    path('event_list/', EventListAPIView.as_view(), name='event-list'),
    path('event_detail/<int:pk>/', EventDetailAPIView.as_view(), name='event-detail'),
    path('event_update/<int:pk>/', EventUpdateAPIView.as_view(), name='event-update'),
    path('event_delete/<int:pk>/', EventDeleteAPIView.as_view(), name='event-delete'),
    path('event_patch/<int:pk>/', EventPatchAPIView.as_view()),
]