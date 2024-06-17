from django.core.paginator import Paginator
from django.contrib import messages
from .forms import PostForm, EditForm
from .models import Profile, Posts, User 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse


@login_required(login_url='login')  #requires user to be logged in to post and view forum
def index(request):
    form1=PostForm()                  #request post form
    if request.method=="POST":         #if post form submitted validate form 
        form1 = PostForm(request.POST)  
        if form1.is_valid():
            post = form1.save(commit=False)  #if form is valid then save info but don't commit
            post.user = request.user          #add user to the save post
            post.save()                      #submit post
            messages.success(request, 'Post created successfully!')
            return redirect('index')         #redirect
        else:
            messages.warning(request, 'Issue with form!') #issue a warning if it doesn't work
    
    posts=Posts.objects.all()        # gets all posts and paginates them when returning a render of the index view
    posts=posts.order_by("-post_date") # order posts by date
    for post in posts:                     # loop through all ordered posts and add a temporary attribute of the number of likes per post
        post.likes_counts=post.likes.count()
    p=Paginator(posts,10)            # paginating
    page_number=request.GET.get('page')
    page_obj=p.get_page(page_number)      
    return render(request, "network/index.html", {'form1':form1, 'page_obj':page_obj})                          

# Display number of followers. number of people that the user follows. Display all posts of profile user in reverser chrnonological order.  Display follow and unfollow button if user is not same user.
@login_required(login_url='login')  #requires user to be logged in to post and view forum
def profile(request, user_id):     # profile page
    viewer = request.user                 # gets logged in users info and profile
    viewer_profile = get_object_or_404(Profile, user=viewer)
    user = get_object_or_404(User, id=user_id) # gets user and profile of user clicked on
    profile = get_object_or_404(Profile, user=user)
    profile_followers= profile.followers.count()
    profile_following= profile.following.count()

    if request.method=="POST":           # Post method to check if users are follownig or followers before submitting requests
        if viewer_profile.user in profile.followers.all():
            viewer_profile.following.remove(profile.user)
            profile.followers.remove(viewer_profile.user)
            
        else:
            viewer_profile.following.add(profile.user)
            profile.followers.add(viewer_profile.user)
            
        viewer_profile.save()
        profile.save()
        return redirect('profile', user_id=user_id)    

    posts=Posts.objects.filter(user=user) # filter posts by user referenced by profile user above
    posts=posts.order_by("-post_date") # order posts by date
    for post in posts:                     # loop through all ordered posts and add a temporary attribute of the number of likes per post
        post.likes_counts=post.likes.count()
    p=Paginator(posts,10)            # paginating
    page_number=request.GET.get('page')
    page_obj=p.get_page(page_number)      
    return render(request, "network/profile.html", {'viewer_profile':viewer_profile, 'profile':profile, 'page_obj':page_obj, 'profile_followers': profile_followers, 'profile_following': profile_following})   # renders profile.html of the user


@login_required(login_url='login')  #requires user to be logged in to post and view forum
def following(request, user_id): # following link
    viewer = request.user                 # gets logged in users info and profile
    viewer_profile = get_object_or_404(Profile, user=viewer)
    posts_list=Posts.objects.none()
    for following in viewer_profile.following.all():
        post=Posts.objects.filter(user=following)
        posts_list=posts_list.union(post)

    posts=posts_list
    if posts: 
        posts=posts.order_by("-post_date") # order posts by date
        for post in posts:                     # loop through all ordered posts and add a temporary attribute of the number of likes per post
            post.likes_counts=post.likes.count()
        p=Paginator(posts,10)            # paginating
        page_number=request.GET.get('page')
        page_obj=p.get_page(page_number)    
        # paginate the page as well with following posts
        return render(request, "network/following.html",{'viewer_profile':viewer_profile, 'page_obj':page_obj})   # renders profile.html of the user
    else:
        return redirect('index')
























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
            profile = Profile(user=user)  # create profile with user 
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
