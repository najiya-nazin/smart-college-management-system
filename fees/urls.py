from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.fee_list,
        name="fee-list"
    ),

    path(
        "create/",
        views.fee_create,
        name="fee-create"
    ),

    path(
        "<int:pk>/",
        views.fee_detail,
        name="fee-detail"
    ),

    path(
        "<int:pk>/edit/",
        views.fee_update,
        name="fee-update"
    ),

    path(
        "<int:pk>/delete/",
        views.fee_delete,
        name="fee-delete"
    ),

]