from django.urls import path
from .views import (
    AddTeacher,
    TeacherList,
    TeacherDetail,
    EditTeacher,
    DeleteTeacher,
)

urlpatterns = [
    path("create/", AddTeacher.as_view(), name="add_teacher"),
    path("list/", TeacherList.as_view(), name="teacher_list"),
    path("<int:pk>/", TeacherDetail.as_view(), name="teacher_detail"),
    path("update/<int:pk>/", EditTeacher.as_view(), name="edit_teacher"),
    path("delete/<int:pk>/", DeleteTeacher.as_view(), name="delete_teacher"),
]