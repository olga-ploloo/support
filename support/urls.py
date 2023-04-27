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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from message.views import MessageViewSet
from ticket.views import TicketViewSet, AssignTicketViewSet
from user.views import ActivateUser, MyTokenObtainPairView, UserLogoutView

router = DefaultRouter()
router.register('tickets', TicketViewSet, basename='ticket')
router.register('assign_ticket', AssignTicketViewSet, basename='assign_ticket')
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
                  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('admin/', admin.site.urls),
                  path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('logout/', UserLogoutView.as_view(), name='logout'),
                  path('auth/', include('djoser.urls.base')),
                  path('auth/activate/<uid>/<token>', ActivateUser.as_view({'get': 'activation'}), name='activation'),
              ] + router.urls

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)
