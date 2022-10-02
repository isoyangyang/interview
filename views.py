from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
import json

from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Follower, Target, Like
from .forms import PostForm


@csrf_exempt
def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    user = request.user
    post_form = PostForm()

    if request.method == "POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post_object = post_form.save(commit=False)
            post_object.author = user
            post_object.save()
            return redirect('index')

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "post_form": post_form,
        "page_obj": page_obj,
    }
    return render(request, "network/index.html", context)


@csrf_exempt
def user(request, target_user):
    logged_in_user = request.user

    clicked_user_profile = User.objects.get(username=target_user)
    clicked_user_posts = clicked_user_profile.post_set.all()
    clicked_user_followers = Follower.objects.filter(follows=clicked_user_profile).count()
    clicked_user_follows = Follower.objects.filter(user=clicked_user_profile).count()

    clicked_user_followers_object = Follower.objects.filter(follows=clicked_user_profile)

    # Paginator details
    paginator = Paginator(clicked_user_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Boolean variable to check whether logged-in user follows target user
    follow_boolean = False
    for follower in clicked_user_followers_object:
        if str(logged_in_user) == str(follower.user) and str(target_user) == str(follower.follows):
            follow_boolean = True
        else:
            follow_boolean = False

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("followed") is True:
            add_follower_record = Follower.objects.create(user=logged_in_user, follows=clicked_user_profile)
            add_follower_record.save()
            follow_boolean = True
            follower_count = Follower.objects.filter(follows=clicked_user_profile).count()
            return JsonResponse({
                "followed": follow_boolean,
                "follower_count": follower_count,
            })

        if data.get("followed") is False:
            delete_follower_record = Follower.objects.filter(user=logged_in_user, follows=clicked_user_profile)
            delete_follower_record.delete()
            follow_boolean = False
            follower_count = Follower.objects.filter(follows=clicked_user_profile).count()
            return JsonResponse({
                "followed": follow_boolean,
                "follower_count": follower_count,
            })

    context = {
        "follow_boolean": follow_boolean,
        "target_user": str(target_user),
        "clicked_user_followers": clicked_user_followers,
        "clicked_user_follows": clicked_user_follows,
        "page_obj": page_obj,
        "logged_in_user": str(logged_in_user),
    }
    return render(request, "network/user.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        print(password)
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def following(request):
    logged_in_user = request.user

    followed_users_posts_list = []

    all_posts = Post.objects.all()
    followed_users = Follower.objects.filter(user=logged_in_user)

    for user in followed_users:
        for post in all_posts:
            if str(user.follows) == str(post.author):
                followed_users_posts_list.append(post)

    print(followed_users, followed_users_posts_list)

    # Paginator details
    paginator = Paginator(followed_users_posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "followed_users_posts": followed_users_posts_list,
    }
    return render(request, "network/following.html", context)


@csrf_exempt
def edit(request, post_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("post") is not None:
            post = Post.objects.get(id=post_id)
            post.post = data.get("post")
            post.save()
            return JsonResponse({
                "edited_body": data.get("post")
            })
    else:
        return render(request, "network/index.html", {})


@csrf_exempt
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)

    if request.method == "GET":
        return JsonResponse(post.serialize())

    print(post, post_id, user)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("like") is True:
            like = Like.objects.create(user=user, post=post)
            like.save()
            post.like_count = Like.objects.filter(post=post).count()
            post.save()
            print(post.like_count)
        else:
            unlike = Like.objects.filter(user=user, post=post)[0]
            unlike.delete()
            post.like_count = Like.objects.filter(post=post).count()
            post.save()
        return JsonResponse({
            "like_count": post.like_count,
        })
        # return HttpResponse(status=204)


