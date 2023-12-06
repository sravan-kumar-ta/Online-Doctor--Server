import random

from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, APIException

from account.customAuth import CustomAuth
from account.models import CustomUser

DEFAULT_PASSWORD = 'Pa$$w0rd!'
ERROR_MESSAGE_TOKEN_INVALID = 'The token is invalid or expired. Please login again.'
ERROR_MESSAGE_SOMETHING_WRONG = 'Something wrong..!'


def generate_username(name):
    username = "".join(name.split(' ')).lower()
    if not CustomUser.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def auth_response(email):
    user = CustomAuth.authenticate(username=email, password=DEFAULT_PASSWORD)

    if user:
        return {
            'username': user.username,
            'email': user.email,
            'tokens': user.tokens()
        }
    else:
        raise AuthenticationFailed(detail=ERROR_MESSAGE_SOMETHING_WRONG)


def register_social_user(provider, email, name, first_name, last_name):
    filtered_user_by_email = CustomUser.objects.filter(email=email)

    if filtered_user_by_email.exists():
        if provider == filtered_user_by_email[0].auth_provider:
            return auth_response(email)
        else:
            raise APIException(
                {'error_message': f'Please continue your login using {filtered_user_by_email[0].auth_provider}'})
    else:
        user = {
            'username': generate_username(name),
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': DEFAULT_PASSWORD
        }
        user = CustomUser.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()
        return auth_response(email)


class Google:
    @staticmethod
    def validate(auth_token):
        try:
            idinfo = id_token.verify_oauth2_token(auth_token, requests.Request())
            if 'accounts.google.com' in idinfo['iss']:
                return idinfo
        except Exception as e:
            return str(e)


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = Google.validate(auth_token)
        if 'sub' not in user_data:
            raise serializers.ValidationError(ERROR_MESSAGE_TOKEN_INVALID)

        user_details = {
            'first_name': user_data['given_name'],
            'last_name': user_data['family_name'],
            'email': user_data['email'],
            'name': user_data['name'],
            'provider': 'google'
        }
        return register_social_user(**user_details)
