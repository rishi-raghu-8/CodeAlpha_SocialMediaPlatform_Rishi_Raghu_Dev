from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm, ProfileForm, RegisterForm
from .models import Comment, Follow, Like, Post, Profile


def ensure_profile(user):
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile


class UserLoginView(LoginView):
    template_name = "social/login.html"
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = "login"


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "social/register.html", {"form": form})


@login_required
def home(request):
    ensure_profile(request.user)

    posts = (
        Post.objects.select_related("author")
        .prefetch_related("likes", "comments__author")
        .annotate(like_count=Count("likes", distinct=True),
                  comment_count=Count("comments", distinct=True))
    )

    following_ids = Follow.objects.filter(
        follower=request.user
    ).values_list("following_id", flat=True)

    # Show own posts and followed users' posts first, then remaining posts.
    feed_posts = posts.filter(
        Q(author=request.user) | Q(author_id__in=following_ids)
    )
    if not feed_posts.exists():
        feed_posts = posts

    liked_ids = set(
        Like.objects.filter(user=request.user, post__in=feed_posts)
        .values_list("post_id", flat=True)
    )

    return render(request, "social/home.html", {
        "posts": feed_posts,
        "liked_ids": liked_ids,
        "post_form": PostForm(),
        "comment_form": CommentForm(),
    })


@login_required
def create_post(request):
    if request.method != "POST":
        return redirect("home")

    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, "Post published!")
    else:
        messages.error(request, "Please check your post.")
    return redirect("home")


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated.")
            return redirect("home")
    else:
        form = PostForm(instance=post)

    return render(request, "social/edit_post.html", {"form": form, "post": post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted.")
    return redirect("home")


@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
    return redirect(request.META.get("HTTP_REFERER", "home"))


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect(request.META.get("HTTP_REFERER", "home"))


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    if request.method == "POST":
        comment.delete()
    return redirect(request.META.get("HTTP_REFERER", "home"))


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile_obj = ensure_profile(user)
    posts = Post.objects.filter(author=user).annotate(
        like_count=Count("likes", distinct=True),
        comment_count=Count("comments", distinct=True),
    )
    followers_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    is_following = (
        request.user != user and
        Follow.objects.filter(follower=request.user, following=user).exists()
    )

    return render(request, "social/profile.html", {
        "profile_user": user,
        "profile_obj": profile_obj,
        "posts": posts,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following,
    })


@login_required
def edit_profile(request):
    profile_obj = ensure_profile(request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile", username=request.user.username)
    else:
        form = ProfileForm(instance=profile_obj)

    return render(request, "social/edit_profile.html", {"form": form})


@login_required
def toggle_follow(request, username):
    target = get_object_or_404(User, username=username)

    if target == request.user:
        messages.warning(request, "You cannot follow yourself.")
        return redirect("profile", username=username)

    if request.method == "POST":
        relation, created = Follow.objects.get_or_create(
            follower=request.user,
            following=target
        )
        if not created:
            relation.delete()

    return redirect("profile", username=username)
