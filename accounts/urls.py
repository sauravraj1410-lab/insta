from django.urls import path
from . import views
from .views import discover_users, follow_toggle, upload_avatar,update_avatar, followers_list, following_list

urlpatterns = [
    path("discover/", discover_users, name="discover"),
    path("follow/<int:user_id>/", follow_toggle, name="follow"),
]
urlpatterns = [
    path("signup/", views.signup_view),
    path("login/", views.login_view),
    path("logout/", views.logout_view),

    path("profile/", views.profile_view),
    path("user/<int:user_id>/", views.user_profile),
    path("follow/<int:user_id>/", views.follow_toggle),
    path("edit/", views.edit_profile),
    path("discover/", discover_users, name="discover"),
    path("follow/<int:user_id>/", follow_toggle, name="follow"),
    path("avatar/", upload_avatar),
    path("avatar/", update_avatar, name="update_avatar"),
    path("followers/<int:user_id>/", followers_list, name="followers"),
    path("following/<int:user_id>/", following_list, name="following"),
]

