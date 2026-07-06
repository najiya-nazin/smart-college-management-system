from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.exam_list,
        name="exam-list"
    ),

    path(
        "create/",
        views.exam_create,
        name="exam-create"
    ),

    path(
        "<int:pk>/",
        views.exam_detail,
        name="exam-detail"
    ),

    path(
        "<int:pk>/edit/",
        views.exam_update,
        name="exam-update"
    ),

    path(
        "<int:pk>/delete/",
        views.exam_delete,
        name="exam-delete"
    ),

]