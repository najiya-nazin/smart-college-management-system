from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.attendance_create, name="attendance_create"),
    path("list/", views.attendance_list, name="attendance_list"),
    path("detail/<int:pk>/", views.attendance_detail, name="attendance_detail"),
    path("update/<int:pk>/", views.attendance_update, name="attendance_update"),
    path("delete/<int:pk>/", views.attendance_delete, name="attendance_delete"),
]