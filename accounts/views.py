from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.serializers import UserSerializer

User = get_user_model()


class UserListView(APIView):
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
