from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from accounts.models import UserProfile
from feeds.models import Post
from feeds.permissions import FollowsOrIsPublic
from .serializers import PostSerializer


class CurrentUserFeedView(ListAPIView):
    """ Returns lists of posts from authors the user follows """
    
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.from_authors_followed_by_user(self.request.user).order_by('-created_at').all()


class SpecificUserFeedView(ListAPIView):
    """ Returns list of Posts for a specific user """

    serializer_class = PostSerializer
    permission_classes = (FollowsOrIsPublic,)

    def get_queryset(self):
        return Post.objects.filter(author__id=self.kwargs['user_id']).order_by('-created_at').all()


class CreatePostView(CreateAPIView):

    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
