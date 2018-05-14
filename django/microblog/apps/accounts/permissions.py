from django.contrib.auth.models import AnonymousUser

from rest_framework.permissions import BasePermission


class UnauthenticatedOnly(BasePermission):

    message = 'Unable to perform action while logged-in.'

    def has_permission(self, request, view):

        if getattr(request, 'user') and not isinstance(request.user, AnonymousUser):
            return False
        return True