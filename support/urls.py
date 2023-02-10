"""support URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path as url
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from message.views import MessageViewSet
from ticket.views import TicketViewSet
from user.views import UserRegistrationView, UserLoginView, UserViewSet

router = DefaultRouter()
router.register('tickets', TicketViewSet, basename='ticket')
router.register('users', UserViewSet, basename='user')
router.register('messages', MessageViewSet, basename='message')

schema_view = get_schema_view(
    openapi.Info(
        title="Support API",
        default_version='v1',
        description="Test description",
    ),
    public=True,
)

urlpatterns = [
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('schema', get_schema_view(
    #     title="Support API",
    #     description="Test description",
    #     version='v1',
    # ), name='api-schema'),
    # path('v1/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('register', UserRegistrationView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.jwt')),
    # path('api/user/', include('user.urls')),
    # path('api/ticket/', include('ticket.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
] + router.urls
