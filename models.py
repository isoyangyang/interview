from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    like_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created']

    def serialize(self):
        return {
            "like_count": self.like_count
        }


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='follower_table_user')
    follows = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='follows')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "follows": self.follows,
            "created": self.created,
        }


class Target(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='target_table_user')
    followedBy = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='followedBy')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "follows": self.followedBy,
            "created": self.created,
        }


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "post": self.post,
            "created": self.created,
        }
