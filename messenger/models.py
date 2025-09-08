from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    TEXT_PREVIEW_LEN = 30

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name="messages")
    user = models.ForeignKey(
        User, related_name="messages", on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return self.text

    @property
    def text_preview(self):
        if len(self.text) > self.TEXT_PREVIEW_LEN:
            return f"{self.text[:self.TEXT_PREVIEW_LEN]}..."

        return self.text
