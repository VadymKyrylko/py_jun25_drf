from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import renderer_classes
from rest_framework.routers import DefaultRouter
from rest_framework.settings import api_settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import UserViewSet

app_name = "accounts"

router = DefaultRouter()

router.register("users", UserViewSet, basename="user")

urlpatterns = router.urls
urlpatterns += [
    path(
        "login/",
        ObtainAuthToken.as_view(renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES),
        name="login",
    ),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
