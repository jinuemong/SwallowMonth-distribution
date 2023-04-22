from django.urls import path, include
from .views import RoutineViewSet,DayRoutineViewSet
from rest_framework.routers import DefaultRouter

router_routine = DefaultRouter()
router_routine.register('routines',RoutineViewSet)
router_routine.register('dayRoutines',DayRoutineViewSet)

urlpatterns = [
    path('',include(router_routine.urls))
]
