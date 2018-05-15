from django.core.exceptions import ObjectDoesNotExist

from rest_framework import permissions

from accounts.models import UserProfile

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user

class FollowsOrIsPublic(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            feed_owner_profile = UserProfile.objects.get(user=view.kwargs['user_id'])
        except ObjectDoesNotExist:
            return False

        # If this is our own feed...
        if feed_owner_profile == request.user.profile:
            return True

        # Ok to view if feed public
        if feed_owner_profile.feed_is_public:
            return True

        # Otherwise check the user is logged-in...
        if not request.user or not request.user.is_authenticated:
            return False

        # ... and they are following the owner of the feed
        return feed_owner_profile in request.user.profile.get_following()
