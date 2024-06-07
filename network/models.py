from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
#Posts
class Posts(models.Model):
    post_text=models.CharField(max_length=130)
    likes=models.ManyToManyField(User,related_name="post_likes", blank=True)
    post_date=models.DateTimeField(db_comment="Date and time when posted",)
    user=models.ForeignKey(User, related_name="post_author", on_delete=models.CASCADE)
   




#Profile
class Profile(models.Model):
    followers=models.ManyToManyField(User,related_name="follower", blank=True)
    following=models.ManyToManyField(User,related_name="following", blank=True)
    user=models.ForeignKey(User,related_name="profile_user", on_delete=models.CASCADE)









