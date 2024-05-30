
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("all_posts", views.all_posts, name="all_posts"),
    path("following/<str:user>", views.following, name="following"),
    path("follower/<str:user>", views.follower, name="follower"),
    path("following_posts/<str:user>", views.following_posts, name="following_posts"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("profile/follow_button/<int:id>/<str:user_id>", views.follow_button, name="follow_button"),
    path("profile/unfollow_button/<int:id>/<str:user_id>", views.unfollow_button, name="unfollow_button"),
    path("edit_post/<int:post_id>/<str:user>", views.edit_post, name="edit_post"),
    path("handle_like", views.handle_like, name="handle_like"),
    path("handle_unlike", views.handle_unlike, name="handle_unlike")

]
