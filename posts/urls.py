from django.urls import include, path
from .views import upload_post, like_post, add_comment

urlpatterns = [
    path('upload/', upload_post, name='upload'),
    path('like/<int:post_id>/', like_post, name='like_post'),
    path('comment/<int:post_id>/', add_comment, name='add_comment'),
    path("stories/", include("stories.urls")),
    
]

