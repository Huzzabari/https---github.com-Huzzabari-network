from django import forms
from .models import Posts



#New Post
class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['post_title', 'post_text']



#Edit Post
class EditForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['post_title', 'post_text']


