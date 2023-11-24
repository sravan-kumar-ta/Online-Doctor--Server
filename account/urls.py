from django.urls import path

from account import views

urlpatterns = [
    path('register/', views.CreateUserView.as_view()),
    path('login/', views.LoginAPIView.as_view())
]
