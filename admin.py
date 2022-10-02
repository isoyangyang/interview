from django.contrib import admin
from .models import User, Post, Follower, Target, Like

# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Follower)
admin.site.register(Target)
admin.site.register(Like)


