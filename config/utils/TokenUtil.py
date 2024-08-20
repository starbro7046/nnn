from django.http import HttpRequest
from django.conf import settings
from challenges.models import Users
import jwt

class TokenUtil(object):
    def extract_token(request: HttpRequest) -> str:
        token = request.headers.get("Authorization")

        return jwt.decode(token.split()[1], settings.SIMPLE_JWT.get('SIGNING_KEY'), algorithms=[settings.SIMPLE_JWT.get('ALGORITHM')])

    def extract_user_id(token):
        user_id = token.get('user_id')

        return user_id

