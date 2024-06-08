from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

#Posts
class Posts(models.Model):
    post_title=models.CharField(max_length=20)
    post_text=models.TextField(max_length=130)
    likes=models.ManyToManyField(User,related_name="post_likes", blank=True)
    post_date=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User, related_name="post_author", on_delete=models.CASCADE)
   
def __str__(self):
    return f"Post:{self.post_text} and Likes:{self.likes} and User: {self.user} from Date:{self.post_date}"




#Profile
class Profile(models.Model):
    followers=models.ManyToManyField(User,related_name="follower", blank=True)
    following=models.ManyToManyField(User,related_name="following", blank=True)
    user=models.ForeignKey(User,related_name="profile_user", on_delete=models.CASCADE)

def __str__(self):
    return f"Followers:{self.followers} and Following:{self.following} and User: {self.user}"







