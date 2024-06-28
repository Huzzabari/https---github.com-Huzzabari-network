
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following/<int:user_id>", views.following, name="following"),  # added following page and users user_id
    path("profile/<int:user_id>", views.profile, name="profile"), # added profile page and users user_id
    path('update_likes/', views.update_likes, name='update_likes'),
    path('edit/<int:post_id>', views.edit_post, name='edit_post')
]
