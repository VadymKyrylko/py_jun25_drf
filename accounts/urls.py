from django.urls import path

from accounts.views import UserListView

app_name = "accounts"

urlpatterns = [
    path("users/", UserListView.as_view(), name="user-list")
]
