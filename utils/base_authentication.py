import jwt
from stocks_project import settings
from utils.reusable_methods import encrypt_token, decrypt_token
from rest_framework import exceptions
from stocks.models import Token
from utils.reusable_methods import *
from rest_framework.authentication import BaseAuthentication
from django.views.decorators.csrf import csrf_exempt


class JWTAuthentication(BaseAuthentication):
    """
        custom authentication class for DRF and JWT
        https://github.com/encode/django-rest-framework/blob/master/rest_framework/authentication.py
    """

    @csrf_exempt
    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            raise exceptions.AuthenticationFailed('Token not provided')
        try:
            access_token = authorization_header.split(' ')[1]
            if not Token.objects.filter(token=access_token, status=1).exists():
                raise exceptions.AuthenticationFailed('Session expired')
            access_token = decrypt_token(access_token)
            payload = jwt.decode(access_token, settings.JWT_ENCODING_SECRET_KEY, algorithms=['HS256'])
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Session expired')
        except jwt.InvalidTokenError:
            raise exceptions.NotAcceptable('Invalid token')

        from stocks.models import User
        user = User.objects.filter(email=payload['email'], is_deleted=False).first()
        if user is None:
            raise exceptions.AuthenticationFailed('Invalid User.')

        return user, None



