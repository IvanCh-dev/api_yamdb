from django.urls import include, path
from rest_framework import routers

from api.views import SignupUserAPIView, TokenAuthApiView

router_v1 = routers.DefaultRouter()

auth_urls = [
    path(r'token/', TokenAuthApiView.as_view()),
    path(r'signup/', SignupUserAPIView.as_view()),
]


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path(r'v1/auth/', include(auth_urls)),
]
