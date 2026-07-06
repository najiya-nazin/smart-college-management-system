from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.marks_list,
        name="marks-list"
    ),

    path(
        "create/",
        views.marks_create,
        name="marks-create"
    ),

    path(
        "<int:pk>/",
        views.marks_detail,
        name="marks-detail"
    ),

    path(
        "<int:pk>/edit/",
        views.marks_update,
        name="marks-update"
    ),

    path(
        "<int:pk>/delete/",
        views.marks_delete,
        name="marks-delete"
    ),

]