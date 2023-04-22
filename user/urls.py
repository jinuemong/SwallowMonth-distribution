from django.urls import path,include
from .views import RegistrationAPIView, LoginAPIView,UpdateProfileView
from .views import UserRetrieveUpdateAPIView,ProfileViewSet , SearchUserView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView
router_user = DefaultRouter()
router_user.register('profile',ProfileViewSet)

urlpatterns = [
    path('register/',RegistrationAPIView.as_view()),
    path('login/',LoginAPIView.as_view()),
    path('current/',UserRetrieveUpdateAPIView.as_view()),
    path('',include(router_user.urls)),
    path('update/profile/',UpdateProfileView.as_view()),
    path('search/profile/',SearchUserView.as_view()),

    #토큰 재발급 
    path("auth/refresh/",TokenRefreshView.as_view()),
    # 토큰 생성
    path("auth/token/",TokenObtainPairView.as_view())
]
