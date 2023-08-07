from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Post, Comment, PostReaction
from .serializers import PostSerializer, CommentSerializer, PostListSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from django.db.models import Count, Q


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.annotate(
        likes_count=Count(
            "reactions", filter=Q(reactions__reaction="like"), distinct=True
        ),
        dislikes_count=Count(
            "reactions", filter=Q(reactions__reaction="dislike"), distinct=True
        ),
    )
    filter_backends = [SearchFilter]
    search_fields = ["title", "content"]

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostSerializer

    def get_permissions(self):
        if self.action in ["create", "destroy", "partial_update"]:
            return [IsAdminUser()]
        elif self.action in ["likes"]:
            return [IsAuthenticated()]
        return []

    def add_or_change_reaction(self, post, user, input_reaction):
        input_reaction = "like" if input_reaction == "like" else "dislike"
        reaction = PostReaction.objects.filter(post=post, user=user).first()
        if reaction is None:
            PostReaction.objects.create(post=post, user=user, reaction=input_reaction)
        elif reaction.reaction == input_reaction:
            reaction.delete()
        else:
            reaction.reaction = "dislike" if reaction.reaction == "like" else "dislike"
            reaction.save()

    @action(methods=["POST"], detail=True, permission_classes=[IsAuthenticated])
    def likes(self, request, pk=None):
        post = self.get_object()
        self.add_or_change_reaction(post, request.user, "like")
        return Response()

    @action(methods=["POST"], detail=True, permission_classes=[IsAuthenticated])
    def dislikes(self, request, pk=None):
        post = self.get_object()
        self.add_or_change_reaction(post, request.user, "dislike")
        return Response()

    @action(methods=["GET"], detail=False)
    def like_top5(self, request):
        queryset = self.get_queryset().order_by("-likes_count")[:5]
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=["GET"], detail=False)
    def dislike_top5(self, request):
        queryset = self.get_queryset().order_by("-dislikes_count")[:5]
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            return [IsOwnerOrReadOnly()]
        return []


class PostCommentViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post = self.kwargs.get("post_id")
        queryset = Comment.objects.filter(post_id=post)
        return queryset

    def create(self, request, post_id=None):
        post = get_object_or_404(Post, id=post_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post)
        return Response(serializer.data)
