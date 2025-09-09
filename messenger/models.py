from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.constraints import UniqueConstraint

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
    image = models.ImageField(null=True, upload_to="uploads/")
    user_likes = models.ManyToManyField(
        User, related_name="liked_messages", through="messenger.Like"
    )

    def __str__(self):
        return self.text

    @property
    def text_preview(self):
        if len(self.text) > self.TEXT_PREVIEW_LEN:
            return f"{self.text[:self.TEXT_PREVIEW_LEN]}..."

        return self.text


class Like(models.Model):
    message = models.ForeignKey(Message, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [UniqueConstraint(fields=["message", "user"], name="unique_like")]
