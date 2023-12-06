from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from account import views
from account.google_auth_view import GoogleSocialAuthView

urlpatterns = [
    path('register/', views.CreateUserView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('logout/', views.LogoutAPIView.as_view()),
    path('user/', views.UserAPIView.as_view()),
    path('change-password/', views.ChangePasswordAPIView.as_view()),
    path('user_by_id/<int:id>/', views.GetUserAPIView.as_view()),
    path('google/', GoogleSocialAuthView.as_view()),
]

# (POST) user/login/ => login with email and password to get token
# (POST) user/register/ => create user
# (GET) user/user/ => get user
# (PATCH) user/user/ => update user
# (PUT) user/change_password/ => change password
# (POST) user/token/refresh/ => refresh token
# (POST) user/logout/ => logout
# (POST) user/google/ => (google) social-auth
