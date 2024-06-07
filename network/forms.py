from django import forms




#New Post
class PostForm(forms.Form):
    #post text
    post_text=forms.CharField(label="post", max_length=130, widget=forms.Textarea)
    #post time and date
    post_date= forms.DateTimeField()








#Edit Post
class EditForm(forms.Form):
    #post text
    post_text=forms.CharField(label="post", max_length=130, widget=forms.Textarea)
    #post time and date
    post_date= forms.DateTimeField()


