from django.urls import path
from .views import (
    add_teacher,
    teacher_list,
    teacher_detail,
    edit_teacher,
    delete_teacher,
    logout_view,
    teacher_dashboard,
)

urlpatterns = [
    path("create/", add_teacher, name="add_teacher"),
    path("teacher_dashboard/",teacher_dashboard, name="teacher_dashboard"),
    path("list/", teacher_list, name="teacher_list"),
    path("detail/<int:pk>/", teacher_detail, name="teacher_detail"),
    path("update/<int:pk>/", edit_teacher, name="edit_teacher"),
    path("delete/<int:pk>/", delete_teacher, name="delete_teacher"),
    path("logout/", logout_view, name="logout"),
]