from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, TasksSummaryView

router = DefaultRouter()
router.register(r"", TaskViewSet)

urlpatterns = [
    path("summary/", view=TasksSummaryView.as_view(), name="tasks_summary"),
    path("", include(router.urls)),
]
