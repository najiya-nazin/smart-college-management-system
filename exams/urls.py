from django.urls import path
from .views import (
    ExamCreateAPIView,
    ExamListAPIView,
    ExamDetailAPIView,
    ExamUpdateAPIView,
    ExamPatchAPIView,
    ExamDeleteAPIView,
)

urlpatterns = [
    path("exam_create/", ExamCreateAPIView.as_view()),
    path("exam_list/", ExamListAPIView.as_view()),
    path("exam_detail/<int:pk>/", ExamDetailAPIView.as_view()),
    path("exam_update/<int:pk>/", ExamUpdateAPIView.as_view()),
    path("exam_patch/<int:pk>/", ExamPatchAPIView.as_view()),
    path("exam_delete/<int:pk>/", ExamDeleteAPIView.as_view()),
]