from django.urls import path
from .views import (
    CreateTimetable,
    TimetableList,
    TimetableDetail,
    UpdateTimetable,
    DeleteTimetable,
)

urlpatterns = [
    path('create/', CreateTimetable.as_view()),
    path('list/', TimetableList.as_view()),
    path('<int:pk>/', TimetableDetail.as_view()),
    path('update/<int:pk>/', UpdateTimetable.as_view()),
    path('delete/<int:pk>/', DeleteTimetable.as_view()),
]