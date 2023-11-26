from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import CustomUserSerializer, LoginSerializer, LogoutSerializer, UserSerializer, \
    ChangePasswordSerializer


class CreateUserView(CreateAPIView):
    model = get_user_model()
    serializer_class = CustomUserSerializer


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)


class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            instance=request.user,
            data=request.data,
            partial=True,
            context={'user': request.user}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'error_message': serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)


class ChangePasswordAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        # Check if the old password matches the current password
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'detail': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        # Set the new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({'detail': 'Password changed successfully'}, status=status.HTTP_200_OK)
