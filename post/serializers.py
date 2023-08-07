from rest_framework import serializers
from .models import *


class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    def get_comments(self, instance):
        serializers = CommentSerializer(instance.comments, many=True)
        return serializers.data

    def get_likes_count(self, instance):
        return PostReaction.objects.filter(post=instance, reaction="like").count()

    def get_dislikes_count(self, instance):
        return PostReaction.objects.filter(post=instance, reaction="dislike").count()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "writer",
            "comments",
            "likes_count",
            "dislikes_count",
            "created_at",
            "updated_at",
        )
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "comments",
        ]


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()

    def get_post(self, instance):
        return instance.post.title

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_field = ["id", "created_at", "update_at", "post"]


class PostListSerializer(serializers.ModelSerializer):
    comments_cnt = serializers.SerializerMethodField()

    def get_comments_cnt(self, instance):
        return instance.comments.count()

    class Meta:
        model = Post
        fields = [
            "id",
            "writer",
            "title",
            "content",
            "created_at",
            "updated_at",
            "comments_cnt",
        ]
        read_only_field = ["id", "created_at", "updated_at", "comments_cnt"]
