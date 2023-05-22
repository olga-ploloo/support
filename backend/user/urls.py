from django.urls import path

from . import views

"""
1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')"""


urlpatterns = [
    path('', views.index, name='index'),
]