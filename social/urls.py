from django.urls import path
from .views import (
    UserLoginView, UserLogoutView, add_comment, create_post, delete_comment,
    delete_post, edit_post, edit_profile, home, profile, register,
    toggle_follow, toggle_like
)

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("post/create/", create_post, name="create_post"),
    path("post/<int:post_id>/edit/", edit_post, name="edit_post"),
    path("post/<int:post_id>/delete/", delete_post, name="delete_post"),
    path("post/<int:post_id>/like/", toggle_like, name="toggle_like"),
    path("post/<int:post_id>/comment/", add_comment, name="add_comment"),
    path("comment/<int:comment_id>/delete/", delete_comment, name="delete_comment"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("profile/<str:username>/", profile, name="profile"),
    path("profile/<str:username>/follow/", toggle_follow, name="toggle_follow"),
]
