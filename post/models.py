from django.db import models

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
    post = models.ForeignKey(Post, blank=False, null=False, on_delete=models.CASCADE, related_name="comments")
    writer = models.CharField(max_length=50)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)