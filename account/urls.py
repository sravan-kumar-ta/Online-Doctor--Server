from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from account import views

urlpatterns = [
    path('register/', views.CreateUserView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('logout/', views.LogoutAPIView.as_view()),
    path('user/', views.UserAPIView.as_view()),
    path('change-password/', views.ChangePasswordAPIView.as_view()),
]
