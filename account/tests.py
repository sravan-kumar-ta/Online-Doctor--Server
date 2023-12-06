from django.test import TestCase

# Create your tests here.
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate

from .customAuth import CustomAuth
from .models import CustomUser


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField()  # Username can be email or username
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['role', 'username', 'get_full_name', 'email', 'password', 'tokens', 'auth_provider']
        read_only_fields = ['username', 'role']  # username & role aren't required in the input data
        extra_kwargs = {'password': {'write_only': True}}  # To avoid returning the password

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        if CustomUser.objects.filter(email=email, auth_provider='google').exists():
            raise serializers.ValidationError('You can log in directly with Google authentication.')

        user = CustomAuth.authenticate(username=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')

        return {
            'role': user.role,
            'email': user.email,
            'tokens': user.tokens,
            'username': user.username,
            'get_full_name': user.get_full_name,
        }
