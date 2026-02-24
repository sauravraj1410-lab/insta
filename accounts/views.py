from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from posts.models import Post
from .models import Profile, Follow


# ---------------- AUTH ----------------
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "accounts/signup.html", {
                "error": "Username already exists"
            })

        if User.objects.filter(email=email).exists():
            return render(request, "accounts/signup.html", {
                "error": "Email already registered"
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        return redirect("/")

    return render(request, "accounts/signup.html")



def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=identifier,
            password=password
        )

        if user is None:
            try:
                username = User.objects.get(email=identifier).username
                user = authenticate(
                    request,
                    username=username,
                    password=password
                )
            except User.DoesNotExist:
                user = None

        if user:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "accounts/login.html", {
                "error": "Invalid credentials"
            })

    return render(request, "accounts/login.html")



def logout_view(request):
    logout(request)
    return redirect("/accounts/login/")


# ---------------- OWN PROFILE ----------------
@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    posts = Post.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "accounts/profile.html", {
        "user_profile": request.user,
        "profile": profile,
        "posts": posts,
        "post_count": posts.count(),
        "followers_count": Follow.objects.filter(following=request.user).count(),
        "following_count": Follow.objects.filter(follower=request.user).count(),
    })


# ---------------- OTHER USER PROFILE ----------------
@login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile, _ = Profile.objects.get_or_create(user=user)

    return render(request, "accounts/user_profile.html", {
        "profile_user": user,
        "profile": profile,
        "posts": Post.objects.filter(user=user),
        "is_following": Follow.objects.filter(
            follower=request.user, following=user
        ).exists(),
        "followers_count": Follow.objects.filter(following=user).count(),
        "following_count": Follow.objects.filter(follower=user).count(),
    })


# ---------------- FOLLOW / UNFOLLOW ----------------
@login_required
def follow_toggle(request, user_id):
    target = get_object_or_404(User, id=user_id)

    if target != request.user:
        obj = Follow.objects.filter(
            follower=request.user, following=target
        )
        if obj.exists():
            obj.delete()
        else:
            Follow.objects.create(
                follower=request.user, following=target
            )

    return redirect(request.META.get("HTTP_REFERER", "/"))


# ---------------- EDIT PROFILE ----------------
@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.bio = request.POST.get("bio", "")
        profile.avatar = request.POST.get("avatar", "")
        profile.save()
        return redirect("/accounts/profile/")

    return render(request, "accounts/edit_profile.html", {
        "profile": profile
    })
@login_required
def discover_users(request):
    users = User.objects.exclude(id=request.user.id)

    following_ids = Follow.objects.filter(
        follower=request.user
    ).values_list("following_id", flat=True)

    return render(request, "accounts/discover.html", {
        "users": users,
        "following_ids": following_ids
    })
@login_required
def upload_avatar(request):
    if request.method == "POST":
        avatar = request.POST.get("avatar")
        profile, _ = Profile.objects.get_or_create(user=request.user)
        profile.avatar = avatar
        profile.save()
        return redirect("/accounts/profile/")
from .models import Profile
from django.contrib.auth.decorators import login_required

@login_required
def update_avatar(request):
    if request.method == "POST":
        avatar_url = request.POST.get("avatar")

        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.avatar = avatar_url
        profile.save()

        return redirect("/accounts/profile/")
@login_required
def followers_list(request, user_id):
    user = get_object_or_404(User, id=user_id)
    followers = Follow.objects.filter(following=user)

    return render(request, "accounts/followers.html", {
        "user_profile": user,
        "followers": followers
    })

@login_required
def following_list(request, user_id):
    user = get_object_or_404(User, id=user_id)
    following = Follow.objects.filter(follower=user)

    return render(request, "accounts/following.html", {
        "user_profile": user,
        "following": following
    })