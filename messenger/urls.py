from django.urls import path
from rest_framework.routers import DefaultRouter

from messenger.views import MessageViewSet, TagViewSet

app_name = "messenger"

router = DefaultRouter()
router.register("messages", MessageViewSet, basename="message")
router.register("tags", TagViewSet, basename="tag")

urlpatterns = router.urls
