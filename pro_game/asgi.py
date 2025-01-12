import os

from decouple import config
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import pro_game.routing
from pro_game.middleware import TokenAuthMiddleware

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    config("DJANGO_SETTINGS_MODULE", default="pro_game.settings.settings"),
)

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": TokenAuthMiddleware(
            URLRouter(pro_game.routing.websocket_urlpatterns)
        ),
    }
)
