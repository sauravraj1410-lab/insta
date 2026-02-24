from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from accounts.models import Profile
from posts.models import Post
from stories.models import Story
from stories.views import story_feed


@login_required
def home(request):
    # Get or create profile (prevents DoesNotExist error)
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Get posts
    posts = Post.objects.all().order_by("-created_at")

    # Get stories (last 7 hours)
    stories = Story.objects.filter(
        created_at__gte=timezone.now() - timedelta(hours=7)
    ).order_by("-created_at")

    # OR if you want to use story_feed view logic:
    # stories = story_feed(request)

    return render(request, "feed.html", {
        "posts": posts,
        "stories": stories,
        "profile": profile
    })
