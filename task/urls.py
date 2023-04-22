from django.urls import path, include
from .views import TaskViewSet
from rest_framework.routers import DefaultRouter

router_task = DefaultRouter()
router_task.register("tasks",TaskViewSet)

urlpatterns = [
    path('',include(router_task.urls))
]
