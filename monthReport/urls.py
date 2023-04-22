from django.urls import path, include
from .views import MonthViewSet, RecordViewSet , RankingViewSet
from rest_framework.routers import DefaultRouter

router_monthData = DefaultRouter()
router_monthData.register("monthDatas",MonthViewSet)
router_monthData.register("recordDatas",RecordViewSet)
router_monthData.register("rankingDatas",RankingViewSet)
urlpatterns = [
    path('',include(router_monthData.urls))
]
