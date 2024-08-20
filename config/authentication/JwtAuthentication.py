from django.conf import settings
from django.http import HttpRequest
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from challenges.models import Users
import jwt


class JwtAuthentication(BaseAuthentication):
    def authenticate(self, request: HttpRequest):
        token = request.headers.get('Authorization')

        if not token:
            return None

        try:
            decode = jwt.decode(token.split()[1], settings.SIMPLE_JWT.get('SIGNING_KEY'),
                                algorithms=[settings.SIMPLE_JWT.get('ALGORITHM')])

            user_id = decode.get('user_id')

            if not user_id:
                return None

            user = Users.objects.get(id=user_id)

            if not user:
                raise AuthenticationFailed("User does not exist")
            return user, None

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Jwt expired")
        except jwt.DecodeError as e:
            raise AuthenticationFailed(f'Jwt decode error: {e}')

