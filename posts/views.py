from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Comment

@csrf_exempt               # 👈 ADD THIS
@login_required
def upload_post(request):
    if request.method == "POST":
        media_url = request.POST.get("media_url")
        caption = request.POST.get("caption")

        if media_url:
            Post.objects.create(
                user=request.user,
                media_url=media_url,
                caption=caption
            )
            return redirect('/')

    return render(request, 'upload.html')


@csrf_exempt
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)

    return redirect('/')


@csrf_exempt
def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        text = request.POST.get("comment")

        if text:
            Comment.objects.create(
                post=post,
                user=request.user,
                text=text
            )
    return redirect('/')
