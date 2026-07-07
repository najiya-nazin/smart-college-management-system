from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.report_create, name="report_create"),
    path("list/", views.report_list, name="report_list"),
    path("detail/<int:pk>/", views.report_detail, name="report_detail"),
    path("update/<int:pk>/", views.report_update, name="report_update"),
    path("delete/<int:pk>/", views.report_delete, name="report_delete"),
]