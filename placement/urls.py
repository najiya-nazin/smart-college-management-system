from django.urls import path
from . import views

urlpatterns = [
    
    path("company/create/", views.company_create, name="company_create"),
    path("company/list/", views.company_list, name="company_list"),
    path("company/detail/<int:pk>/", views.company_detail, name="company_detail"),
    path("company/update/<int:pk>/", views.company_update, name="company_update"),
    path("company/delete/<int:pk>/", views.company_delete, name="company_delete"),

    
    path("placement/create/", views.placement_create, name="placement_create"),
    path("placement/list/", views.placement_list, name="placement_list"),
    path("placement/detail/<int:pk>/", views.placement_detail, name="placement_detail"),
    path("placement/update/<int:pk>/", views.placement_update, name="placement_update"),
    path("placement/delete/<int:pk>/", views.placement_delete, name="placement_delete"),
]