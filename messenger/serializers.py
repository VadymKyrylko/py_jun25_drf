from django.contrib.auth import get_user_model
from rest_framework import serializers

from base.serializers import CreatableSlugRelatedField
from messenger.models import Message, Tag

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")
        read_only_fields = fields


class MessageSerializer(serializers.ModelSerializer):
    tags = CreatableSlugRelatedField(
        slug_field="name", many=True, queryset=Tag.objects.all(), required=False
    )

    class Meta:
        model = Message
        fields = ("id", "text", "created_at", "tags", "user")
        read_only_fields = ("id", "created_at", "user")


class MessageListSerializer(MessageSerializer):
    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Message
        fields = ("id", "text_preview", "created_at", "user_username", "tags")


class MessageDetailSerializer(MessageSerializer):
    user = UserSerializer(read_only=True)
