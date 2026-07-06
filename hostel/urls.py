from django.urls import path
from . import views

urlpatterns = [

    path("", views.hostel_list, name="hostel-list"),
    path("create/", views.hostel_create, name="hostel-create"),
    path("<int:pk>/", views.hostel_detail, name="hostel-detail"),
    path("<int:pk>/edit/", views.hostel_update, name="hostel-update"),
    path("<int:pk>/delete/", views.hostel_delete, name="hostel-delete"),

    path("rooms/", views.room_list, name="room-list"),
    path("rooms/create/", views.room_create, name="room-create"),
    path("rooms/<int:pk>/", views.room_detail, name="room-detail"),
    path("rooms/<int:pk>/edit/", views.room_update, name="room-update"),
    path("rooms/<int:pk>/delete/", views.room_delete, name="room-delete"),

]