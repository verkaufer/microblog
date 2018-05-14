from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError as DRFValidationError

from accounts.models import UserProfile, RELATION_TYPES, FOLLOWING
from .exceptions import LoginFailed

class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()

    def validate_username(self, username):

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise LoginFailed("Invalid authentication credentials.")

        return username

    def validate(self, attrs):
        # validate user and password are valid and match
        user = authenticate(username=attrs['username'], password=attrs['password'])

        if user is None:
            raise LoginFailed("Invalid authentication credentials.")

        attrs['authenticated_user'] = user
        return attrs


class RegisterSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_username(self, username):

        user_with_username = User.objects.filter(username=username)

        if user_with_username.exists():
            raise DRFValidationError

        return username

    def save(self):
        new_user = User.objects.create_user(
            username=self.validated_data['username'],
            password=self.validated_data['password'],
        )

        # Create our user profile at the same time
        user_profile = UserProfile.objects.create(user=new_user)

        login(self.context.get('request'), new_user)


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        exclude = ('user', 'id', 'following')


class FollowUserSerializer(serializers.Serializer):

    user_to_follow = serializers.IntegerField()
    follow_type = serializers.ChoiceField(choices=RELATION_TYPES)

    def validiate_user_to_follow(self, user_to_follow):
        try:
            User.objects.get(pk=user_to_follow)
        except User.DoesNotExist:
            raise DRFValidationError("User you are trying to follow does not exist.")

        return user_to_follow

    def save(self):
        current_user = self.context['request'].user
        user_to_follow_profile, _ = UserProfile.objects.get_or_create(user__id=self.validated_data['user_to_follow'])

        current_user.profile.add_relation(user_to_follow_profile, FOLLOWING)





