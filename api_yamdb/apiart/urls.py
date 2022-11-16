from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apiart.views import TitleViewSet


v1_router = DefaultRouter()
v1_router.register(r'titles', TitleViewSet, basename='titles')
app_name = 'apiart'

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include('apiart.jwt_token')),
]