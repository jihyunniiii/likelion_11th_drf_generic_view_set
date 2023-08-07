from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    writer = models.CharField(max_length=50)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(
        Post, blank=False, null=False, on_delete=models.CASCADE, related_name="comments"
    )
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PostReaction(models.Model):
    REACTION_CHOICES = (("like", "Like"), ("dislike", "Dislike"))
    reaction = models.CharField(choices=REACTION_CHOICES, max_length=10)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reactions")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
