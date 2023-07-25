from rest_framework import serializers
from .models import *

class PostSerializer(serializers.ModelSerializer):
    def get_comments(self, instance):
        serializers = CommentSerializer(instance.comments, many=True)
        return serializers.data

    class Meta:
        model = Post
        fields = '__all__'
        read_only_field = ['id', 'created_at', 'updated_at', 'comments', 'like']

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()

    def get_post(self, instance):
        return instance.post.title
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_field = ['id', 'created_at', 'update_at', 'post']

class PostListSerializer(serializers.ModelSerializer):
    comments_cnt = serializers.SerializerMethodField()

    def get_comments_cnt(self, instance):
        return instance.comments.count()
    
    class Meta:
        model = Post
        fields = ['id','writer','created_at','updated_at','comments_cnt']
        read_only_field = ['id', 'created_at', 'updated_at','comments_cnt']