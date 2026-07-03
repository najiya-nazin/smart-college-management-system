from django.urls import path
from .views import (
    AddMarks,
    MarksList,
    MarksDetail,
    EditMarks,
    DeleteMarks,
)

urlpatterns = [
    path("create/", AddMarks.as_view(), name="add_marks"),
    path("list/", MarksList.as_view(), name="marks_list"),
    path("<int:pk>/", MarksDetail.as_view(), name="marks_detail"),
    path("update/<int:pk>/", EditMarks.as_view(), name="edit_marks"),
    path("delete/<int:pk>/", DeleteMarks.as_view(), name="delete_marks"),
]