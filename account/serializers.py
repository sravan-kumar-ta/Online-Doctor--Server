from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .customAuth import CustomAuth
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'full_name',
                  'email', 'gender', 'role', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')

        if password and password2 and password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})

        return data

    def create(self, validated_data):
        password = validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['role', 'username', 'get_full_name', 'email', 'password', 'tokens']
        read_only_fields = ['username', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
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
