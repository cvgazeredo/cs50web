import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core import serializers


from .models import User, Post, Follower, Following, Like

def countLikes(posts, user) :
    for post in posts:
        likesCount = Like.objects.filter(post=post).count()
        post.likesCount = likesCount
        post.isLiked = Like.objects.filter(post=post, userliked=user).exists()


def index(request):
    if request.user.is_authenticated:
        # Check user posts:
        user = request.user
        posts = Post.objects.filter(user=user).order_by("-date")
               
        countLikes(posts, user)

        # # Check followings of user: 
        countFollowings = Following.objects.filter(user=user)

        # #Check followers of user:
        countFollowers = Follower.objects.filter(user=user)

        # # Paginator:
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)

        return render(request, "network/index.html", { "posts": posts, "user": user, "followings": countFollowings, "followers": countFollowers})

    return render(request, "network/login.html")

@login_required
def new_post(request):
    if request.method == "POST":
        user = request.user
        text = request.POST["text"]
        print(text)

        new_post = Post(user=user,
        text=text)
        new_post.save()
    
    return HttpResponseRedirect(reverse("index"))

@login_required
def all_posts(request):
    if request.user.is_authenticated:
        user = request.user
        posts = Post.objects.order_by("-date")
        
        countLikes(posts, user)
        
        # Paginator:
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)

        return render(request, "network/all_posts.html", { "posts": posts, "user": user})

    return render(request, "network/login.html")


def following(request, user):
    user = request.user
    allfollowing = Following.objects.all()
    followings = allfollowing.filter(user=user)

    allfollowers = Follower.objects.all()
    followers = allfollowers.filter(user=user)

    return render(request, "network/following.html", { "followings": followings, "followers": followers } )

def follower(request, user):
    user = request.user
    allfollowers = Follower.objects.all()
    followers = allfollowers.filter(user=user)

    allfollowing = Following.objects.all()
    followings = allfollowing.filter(user=user)

    return render(request, "network/follower.html", { "followers": followers, "followings": followings } )

def following_posts(request, user):
    main_user = request.user

    # List all followings users:
    all_followings = Following.objects.filter(user=main_user)
    
    all_posts = Post.objects.all().order_by("-date")

    # Filter posts by user's followings:
    posts = []

    for post in all_posts:
        for following in all_followings:
            if post.user == following.following:
                posts.append(post)    
    
    # Check likes:
    countLikes(posts, main_user)
     
    # Paginator:
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(page_obj)

    return render(request, "network/following_posts.html", {
    "posts": posts,
    "page_obj": page_obj,
    "user": user,
    })

@login_required
def edit_post(request, post_id, user):
    if request.method == 'POST':
        print("NAOOOOOOOOOOOOOOOOOOOOOOOOOOO ENTROU AQUI")
        original_post = Post.objects.get(pk=post_id)
        edited_text = request.POST["text"]
        
        original_post.text = edited_text

        original_post.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        print(user)
        post_to_edit = Post.objects.get(id=post_id)
        print(post_to_edit)
        return render(request, "network/edit_post.html", { "post_to_edit":post_to_edit})

def profile(request, id):
    user = request.user
    # Check user id:
    user_id = User.objects.get(pk=id)
    print(f"thats user_id {user_id}")

    # Render in chronological order posts of user
    user_post = Post.objects.all()
    posts = user_post.order_by("-date").filter(user=id)

    # Render following of profile user:
    allfollowing = Following.objects.all()
    followings = allfollowing.filter(user=id)
    print(f"This user: {id} have this followers: {followings}")

    # Render followers of profile user:
    allfollowers = Follower.objects.all()
    followers = allfollowers.filter(user=id)
    print(f"This user: {id} have this followers: {followers}")

    # Check if logged user is same as profile use 
    if request.user.is_authenticated:
        if request.user == user_id:
            print("Logged user cannot follow their own profile")
            sameUser = True
        else:
            sameUser = False
        

    # Check if logged user is following profile user:
    if request.user.is_authenticated:
        follow_unfollow = allfollowing.filter(user=request.user, following=user_id)
        print(follow_unfollow)
        if follow_unfollow:
            isFollowing = True
            print("User following this profile")
        else:
            isFollowing = False
            print("User not following this profile")
        print(isFollowing)

    # Check likes:
    likes = Like.objects.all()

    countLikes(posts, user)

    # Paginator:
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "user_id": user_id,
        "posts": posts,
        "followings": followings,
        "followers": followers,
        "isFollowing": isFollowing,
        "id": id,
        "sameUser": sameUser,
         } )

@login_required
def follow_button(request, id, user_id):
    test = Following.objects.all()
    print(f"TESTIIIING {test}")

    follow_user = Following(
        user=request.user, 
        following=User.objects.get(username=user_id)
    )
    print(follow_user)

    followed = Follower(user=User.objects.get(username=user_id),
    follower=User.objects.get(username=request.user)
    )
    print(followed)

    follow_user.save()
    followed.save()

    print(f"Logged user is now following {user_id}")
    return HttpResponseRedirect(reverse("profile", kwargs={"id": id}))

@login_required
def unfollow_button(request, id, user_id):

    unfollow_user = Following.objects.get(user=request.user, following=User.objects.get(username=user_id))
    print(unfollow_user)
    unfollow_user.delete()

    followed = Follower.objects.get(user=User.objects.get(id=id), follower=User.objects.get(username=request.user))

    print(followed)
    followed.delete()

    return HttpResponseRedirect(reverse("profile", kwargs={"id": id}))



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

def handle_like(request):
    print("Function handle_like reached!")
    # Get user id of user that liked post:
    user = request.user

    # Get post id 
    data = json.loads(request.body)
    post_id = data.get("post_id")
    
    # Get user id of posting
    user_id_of_post = Post.objects.get(id=post_id).user

    # Save like
    liked = Like(
        user=user_id_of_post,
        post=Post.objects.get(id=post_id),
        userliked=user
    )
    liked.save()

    return JsonResponse({"message": "Success"}, status=201)

def handle_unlike(request):
    print("Function handle_unlike reached!")
    # Get user id of user that liked post:
    user = request.user

    # Get post id 
    data = json.loads(request.body)
    post_id = data.get("post_id")
    
    # Get user id of posting
    user_id_of_post = Post.objects.get(id=post_id).user

    unlike = Like.objects.filter(post=post_id, userliked=user)
    print(unlike)
    unlike.delete()
    # Delete like


    return JsonResponse({"message": "Success"}, status=201)