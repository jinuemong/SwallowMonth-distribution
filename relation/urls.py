from .views import FUserViewSet,FriendShipViewSet,AlarmView
from . views import MessageViewSet, MessageListView, CheckFriendView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RandomUserView,FriendListView
router_routine = DefaultRouter()
router_routine.register('friendShips',FriendShipViewSet)
router_routine.register('fusers',FUserViewSet)
router_routine.register('messages',MessageViewSet)

urlpatterns = [
    path('alarms/',AlarmView.as_view()),
    path('friends/',FriendListView.as_view()),
    path('messageList/',MessageListView.as_view()),
    path('randomProfile/',RandomUserView.as_view()),
    path('checkFriendShip/',CheckFriendView.as_view()),
    path('',include(router_routine.urls)),
]
