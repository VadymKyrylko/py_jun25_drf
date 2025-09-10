from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()


class TestMessageViews(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")

    def test_message_list(self):
        self.client.force_authenticate(user=self.user)
        ...
