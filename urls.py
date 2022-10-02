
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<str:target_user>", views.user, name="user"),
    path("following", views.following, name="following"),
    path("edit/<str:post_id>", views.edit, name="edit"),
    path("like/<str:post_id>", views.like, name="like"),

]
