from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "is_staff", "password")
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        email = validated_data.pop("email", instance.email)
        username = validated_data.pop("username", instance.username)

        instance.email = email
        username.username = username

        # for key in ("username", "email"):
        #     setattr(instance, key, validated_data.get(key, instance.key))

        if password:
            instance.set_password(password=password)

        instance.save()

        return instance
