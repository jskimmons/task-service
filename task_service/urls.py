from django.urls import path, include

urlpatterns = [
    path("tasks/", include("tasks.urls")),
    path("users/", include("users.urls")),
]
