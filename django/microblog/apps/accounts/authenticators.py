from django.contrib.auth.models import AnonymousUser

from rest_framework.authentication import BaseAuthentication


class NoAuthForRegistration(BaseAuthentication):

    def authenticate(self, request):
        return AnonymousUser, None