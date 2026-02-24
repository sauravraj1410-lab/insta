from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import Follow
from .models import Chat, Message

@login_required
def chat_list(request):
    following = Follow.objects.filter(
        follower=request.user
    ).values_list("following_id", flat=True)

    followers = Follow.objects.filter(
        following=request.user
    ).values_list("follower_id", flat=True)

    mutual_ids = set(following).intersection(set(followers))
    users = User.objects.filter(id__in=mutual_ids)

    return render(request, "chat/chat_list.html", {
        "users": users
    })


@login_required
def chat_detail(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    # 🔐 must be mutual followers
    is_mutual = (
        Follow.objects.filter(follower=request.user, following=other_user).exists()
        and
        Follow.objects.filter(follower=other_user, following=request.user).exists()
    )

    if not is_mutual:
        return redirect("/chat/")

    # ensure unique chat
    user1, user2 = sorted(
        [request.user, other_user],
        key=lambda u: u.id
    )

    chat, _ = Chat.objects.get_or_create(
        user1=user1,
        user2=user2
    )

    messages = Message.objects.filter(chat=chat).order_by("created_at")

    if request.method == "POST":
        text = request.POST.get("text")
        if text:
            Message.objects.create(
                chat=chat,
                sender=request.user,
                text=text
            )
        return redirect(f"/chat/{other_user.id}/")

    return render(request, "chat/chat_detail.html", {
        "other_user": other_user,
        "messages": messages
    })
