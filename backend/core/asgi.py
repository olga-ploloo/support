import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import OriginValidator
from django.core.asgi import get_asgi_application

import support.urls
from backend.core.middleware.JWTAuthMiddleware import JwtAuthMiddlewareStack

django_asgi_app = get_asgi_application()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "support.settings")

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket":
        OriginValidator(
            JwtAuthMiddlewareStack(URLRouter(
                support.urls.websocket_urlpatterns
            )), ['*'],
        )
})
