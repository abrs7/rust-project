from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/status", views.status_view, name="status"),
    path("api/data", views.data_view, name="data"),
]