from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TaskViewSet

app_name = "v1"

router = DefaultRouter()
router.register("tasks", TaskViewSet, basename="tasks")

urlpatterns = [
    path("", include(router.urls)),
]
