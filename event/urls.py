from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.event_list,
        name="event-list"
    ),

    path(
        "create/",
        views.event_create,
        name="event-create"
    ),

    path(
        "<int:pk>/",
        views.event_detail,
        name="event-detail"
    ),

    path(
        "<int:pk>/edit/",
        views.event_update,
        name="event-update"
    ),

    path(
        "<int:pk>/delete/",
        views.event_delete,
        name="event-delete"
    ),

]