from django.db import models
from django.contrib.auth.models import User

class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stories")
    media_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    likes = models.ManyToManyField(
        User, related_name="liked_stories", blank=True
    )

    views = models.ManyToManyField(
        User, related_name="viewed_stories", blank=True
    )

    def total_likes(self):
        return self.likes.count()

    def total_views(self):
        return self.views.count()

    def __str__(self):
        return f"{self.user.username} story"
