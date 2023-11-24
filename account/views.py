from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView

from account.serializers import CustomUserSerializer


class CreateUserView(CreateAPIView):
    model = get_user_model()
    serializer_class = CustomUserSerializer
