from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_timetable, name="create_timetable"),
    path("list/", views.timetable_list, name="timetable_list"),
    path("detail/<int:pk>/", views.timetable_detail, name="timetable_detail"),
    path("update/<int:pk>/", views.update_timetable, name="update_timetable"),
    path("delete/<int:pk>/", views.delete_timetable, name="delete_timetable"),
]