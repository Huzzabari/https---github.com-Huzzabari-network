from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

#Posts
class Posts(models.Model):
    post_title=models.CharField(max_length=20) #title
    post_text=models.TextField(max_length=330) #text
    likes=models.ManyToManyField(User,related_name="post_likes", blank=True) #likes, will be many users
    post_date=models.DateTimeField(auto_now_add=True) #date/time
    user=models.ForeignKey(User, related_name="post_author", on_delete=models.CASCADE) #user id foreign key
   
def __str__(self):
    return f"Post:{self.post_text} and Likes:{self.likes} and User: {self.user} from Date:{self.post_date}"




#Profile
class Profile(models.Model):
    followers=models.ManyToManyField(User,related_name="follower", blank=True) #who is following them
    following=models.ManyToManyField(User,related_name="following", blank=True) #who they are following
    user=models.ForeignKey(User,related_name="profile_user", on_delete=models.CASCADE) #user id foreign key

def __str__(self):
    return f"Followers:{self.followers} and Following:{self.following} and User: {self.user}"







