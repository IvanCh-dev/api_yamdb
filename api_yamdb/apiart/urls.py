from apiart.views import CategoryViewSet, GenreViewSet, TitleViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

v1_router = DefaultRouter()
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')
app_name = 'apiart'

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]