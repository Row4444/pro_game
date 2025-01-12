from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed


@database_sync_to_async
def get_user_from_token(token: bytes):
    """ Get user from token or AnonymousUser """
    try:
        jwt_auth = JWTAuthentication()
        validated_token = jwt_auth.get_validated_token(token)
        user = jwt_auth.get_user(validated_token)
        return user
    except (InvalidToken, AuthenticationFailed):  # raise from get_validated_token / get_user
        return AnonymousUser()


#  https://channels.readthedocs.io/en/latest/topics/authentication.html#django-authentication
class TokenAuthMiddleware(BaseMiddleware):
    """ Check header for the jwt auth in ws """
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        token_key = None
        for key, value in scope["headers"]:
            if key.decode() == "authorization":  # header (b'authorization', b'<JWT>')
                token_key = value
                break

        scope["user"] = await get_user_from_token(token_key)
        return await self.inner(scope, receive, send)
