from django.urls import path
from .views import upload_story, story_view, like_story, story_analytics

urlpatterns = [
    path("upload/", upload_story, name="upload_story"),
    path("<int:story_id>/", story_view, name="story_view"),
    path("like/<int:story_id>/", like_story, name="like_story"),
    path("analytics/<int:story_id>/", story_analytics, name="story_analytics"),

]
