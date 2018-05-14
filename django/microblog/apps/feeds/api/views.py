from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin
from rest_framework import status
from rest_framework.response import Response

from accounts.models import UserProfile
from feeds.models import Post
from feeds.permissions import IsOwnerOrReadOnly
from .serializers import FeedSerializer, PostSerializer


class FeedView(ListAPIView):

    serializer_class = PostSerializer

    def get_queryset(self):
        # using current user
        # get all people user is following
        # get all their posts
        # TODO: Add in reverse chronological order
        if 'user_id' not in self.kwargs:
            return Post.objects.from_authors_followed_by_user(self.request.user)

        return Post.objects.filter(author__id=self.kwargs['user_id']).order_by('-created_at').all()


    def get(self, request, *args, **kwargs):
        if kwargs.get('user_id'):
            feed_owner_profile = UserProfile.objects.get(user=kwargs['user_id'])

            if not feed_owner_profile.feed_is_public and \
                self.request.user.profile not in feed_owner_profile.get_followers():
                    return Response({'detail': "Feed is viewable only by followers"}, status=status.HTTP_401_UNAUTHORIZED)
        return super().get(request, *args, **kwargs)


class CreatePostView(CreateAPIView):

    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
