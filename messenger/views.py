from django.core.exceptions import ValidationError
from django_filters import rest_framework as rest_filters
from rest_framework import filters, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, action
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from base.filter_backends import IsOwnerFilterBackend
from messenger.filters import MessageFilter
from messenger.models import Message, Tag
from messenger.serializers import (
    MessageDetailSerializer,
    MessageListSerializer,
    MessageSerializer,
    TagSerializer,
)

# @api_view(["GET", "POST"])
# def message_list(request: Request) -> Response:
#     if request.method == "GET":
#         messages = Message.objects.all()
#
#         serializer = MessageSerializer(messages, many=True)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     if request.method == "POST":
#         serializer = MessageSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class MessageListView(APIView):
#     def get(self, request: Request) -> Response:
#         messages = Message.objects.all()
#
#         serializer = MessageSerializer(messages, many=True)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request: Request) -> Response:
#         serializer = MessageSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class TagListView(APIView):
#     def get(self, request: Request) -> Response:
#         tags = Tag.objects.all()
#
#         serializer = TagSerializer(tags, many=True)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request: Request) -> Response:
#         serializer = TagSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# ------------------------------------------------ CUSTOM GENERICS ---------------------------------------------
# class CustomGenericView(APIView):
#     queryset = None
#     serializer_class = None
#
#     def get_queryset(self):
#         assert self.queryset is not None, "queryset attribute is required"
#
#         return self.queryset.all()
#
#     def get_serializer_class(self):
#         assert self.serializer_class, "serializer_class attribute is required"
#
#         return self.serializer_class
#
#
# class CreateMixin:
#     def create(self, request: Request) -> Response:
#         serializer = self.get_serializer_class()(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class ListMixin:
#     def list(self, request: Request) -> Response:
#         queryset = self.get_queryset()
#
#         serializer = self.get_serializer_class()(queryset, many=True)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# class BaseListCreateView(ListMixin, CreateMixin, CustomGenericView):
#     def get(self, request: Request) -> Response:
#         return self.list(request)
#
#     def post(self, request: Request) -> Response:
#        return self.create(request)
#
#
# class MessageListView(BaseListCreateView):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer
#
#
# class TagListView(ListMixin, CustomGenericView):
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
#
#     def get(self, request: Request) -> Response:
#         return self.list(request)


# ----------------------------------------------------ViewSets---------------------------------------------------
class MessageViewSet(ModelViewSet):
    filter_backends = (
        filters.SearchFilter,
        rest_filters.DjangoFilterBackend,
        filters.OrderingFilter,
    )
    search_fields = ("text", "user__username", "tags__name")
    filterset_class = MessageFilter
    ordering_fields = ("created_at",)
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return (
            Message.objects.select_related("user")
            .prefetch_related("tags")
            .prefetch_related("user_likes")
        )

    def get_serializer_class(self):
        if self.action == "list":
            return MessageListSerializer

        if self.action == "retrieve":
            return MessageDetailSerializer

        return MessageSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["POST"], serializer_class=None)
    def like(self, request, pk=None):
        message = self.get_object()
        user = request.user

        if message.user_likes.filter(id=user.id).exists():
            message.user_likes.remove(user)
        else:
            message.user_likes.add(user)

        serializer = MessageListSerializer(message)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
