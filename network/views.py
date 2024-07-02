from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib import messages
from .forms import PostForm, EditForm
from .models import Profile, Posts, User 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


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
        post.likers=[user.id for user in post.likes.all()]
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
        post.likers=[user.id for user in post.likes.all()]
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
            post.likers=[user.id for user in post.likes.all()]
        p=Paginator(posts,10)            # paginating
        page_number=request.GET.get('page')
        page_obj=p.get_page(page_number)    
        # paginate the page as well with following posts
        return render(request, "network/following.html",{'viewer_profile':viewer_profile, 'page_obj':page_obj})   # renders profile.html of the user
    else:
        return redirect('index')


@csrf_exempt  #using javascript so exempt 
def update_likes(request):      # update likes view
    if request.method == 'POST':        # if method is post
        heart=False
        data = json.loads(request.body)     # reques the body and store in variable data
        user_id = data['likes']    # store the user that liked the post 
        post_id = data['post']      # store the user who made the post
        try:
            user = User.objects.get(id=user_id)  # get user object based on user id
            post = Posts.objects.get(id=post_id) # get post object based on the post id
        except (User.DoesNotExist, Posts.DoesNotExist):
            messages.warning(request, 'User or Post doesnt exist!')
            return redirect('index')
        # Handle the case where the user or post does not exist
        if user in post.likes.all():   # if the user is in any of the post likes then remove the user
            post.likes.remove(user)
            heart=True
        else:
            post.likes.add(user)     # otherwise add user
            heart=False
        post.save() #save to update this
        return JsonResponse({'new_likes_count': post.likes.count(), 'heart':heart})     # return the new likes count by checking the post object.likes and using the count method.
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



@csrf_exempt  #using javascript so exempt 
def edit_post(request, post_id):      # update likes view
    if request.method == 'GET':        # if method is get
        post= get_object_or_404(Posts, id=post_id)  #get post object based on post_id
        form=post.post_text
        return JsonResponse({'form': form}) #return my template with data from instance
     
    elif request.method == 'POST':      # if post request for submission
       data=json.loads(request.body)   #request the body, which gives me the data
       postId=data['postId']          # store the postid at the postid
       text=data['text']              # store the text as text
       post = get_object_or_404(Posts, id=postId)   #get the instance of the post object tied to the post id
       post.post_text = text  #update the post text
       post.save()        #save it
       return JsonResponse({'success': True, "data":data}) #returrn the response of success and the info for javascript to use
    


















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
