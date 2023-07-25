from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, PostListSerializer

# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    
    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostSerializer

class CommentViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class PostCommentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = self.kwargs.get("post_id")
        queryset = Comment.objects.filter(post_id = post)
        return queryset
    
    def create(self, request, post_id=None):
        post = get_object_or_404(Post, id=post_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post)
        return Response(serializer.data)