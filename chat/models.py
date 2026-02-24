from django.contrib.auth.models import User
from django.db import models

class Chat(models.Model):
    user1 = models.ForeignKey(
        User,
        related_name="chat_user1",
        on_delete=models.CASCADE
    )
    user2 = models.ForeignKey(
        User,
        related_name="chat_user2",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user1", "user2")

    def __str__(self):
        return f"{self.user1} ↔ {self.user2}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.text[:20]}"
