from django.contrib.auth import login, logout

from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from accounts.permissions import UnauthenticatedOnly
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

    permission_classes = (IsAuthenticated, )

    serializer_class = ProfileSerializer

    def get_object(self):

        return UserProfile.objects.get(user=self.request.user)


class FollowUserView(GenericAPIView):

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


