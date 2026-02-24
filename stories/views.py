from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from .models import Story
from accounts.models import Follow


@login_required
def upload_story(request):
    if request.method == "POST":
        media_url = request.POST.get("media_url")

        Story.objects.create(
            user=request.user,
            media_url=media_url,
            expires_at=timezone.now() + timedelta(hours=24)
        )

        return redirect("/")

    return render(request, "stories/upload.html")


@login_required
def story_feed(request):
    following_ids = Follow.objects.filter(
        follower=request.user
    ).values_list("following_id", flat=True)

    stories = Story.objects.filter(
        user__id__in=list(following_ids) + [request.user.id],
        expires_at__gt=timezone.now()
    ).order_by("-created_at")

    return stories


@login_required
def story_view(request, story_id):
    story = get_object_or_404(Story, id=story_id)

    # Allow only followers or owner
    is_follower = Follow.objects.filter(
        follower=request.user,
        following=story.user
    ).exists()

    if story.user != request.user and not is_follower:
        return redirect("/")

    # ADD VIEW (only once)
    if request.user != story.user:
        story.views.add(request.user)

    return render(request, "stories/view.html", {
        "story": story
    })


@login_required
def like_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)

    if request.user in story.likes.all():
        story.likes.remove(request.user)
    else:
        story.likes.add(request.user)

    return redirect(f"/stories/{story.id}/")
@login_required
def story_analytics(request, story_id):
    story = get_object_or_404(Story, id=story_id)

    if request.user != story.user:
        return redirect("/")

    viewers = story.views.all()

    return render(request, "stories/analytics.html", {
        "story": story,
        "viewers": viewers
    })
