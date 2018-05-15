from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed

from feeds.permissions import IsOwnerOrReadOnly

from accounts.authenticators import NoAuthForRegistration
from accounts.models import UserProfile, FOLLOWING
from .serializers import LoginSerializer, RegisterSerializer, ProfileSerializer, FollowUserSerializer


class LoginView(GenericAPIView):

    authentication_classes = ()
    permission_classes = ()

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        login(request, serializer.validated_data['authenticated_user'])
        return Response({'auth': 'ok'}, status=status.HTTP_200_OK)


class LogoutView(APIView):

    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class RegisterView(CreateAPIView):
    authentication_classes = (NoAuthForRegistration,)
    permissions_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ProfileView(RetrieveUpdateAPIView):
    """ Return the Profile data for requested user """
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = ProfileSerializer
    lookup_url_kwarg = 'username'

    def get_object(self):
        # Allow user to see own profile via `/me` kwarg
        if self.kwargs[self.lookup_url_kwarg] == "me":
            if self.request.user and self.request.user.is_authenticated:
                return self.request.user.profile

        return get_object_or_404(
            UserProfile.objects.filter(user__username__iexact=self.kwargs[self.lookup_url_kwarg])
        )

    def put(self, request, *args, **kwargs):
        raise MethodNotAllowed


class FollowUserView(GenericAPIView):
    """ Create new Follow relation or delete existing follow relation """
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowUserSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile_to_follow, _ = UserProfile.objects.get_or_create(user__id=serializer.data['user_to_follow'])

        request.user.profile.add_relation(profile_to_follow, FOLLOWING)
        return Response(status=status.HTTP_201_CREATED)
    
    def delete(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile_to_unfollow, _ = UserProfile.objects.get_or_create(user__id=serializer.data['user_to_follow'])

        request.user.profile.remove_relation(profile_to_unfollow, FOLLOWING)
        return Response(status=status.HTTP_204_NO_CONTENT)

