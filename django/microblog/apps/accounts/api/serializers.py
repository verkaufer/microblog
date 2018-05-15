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
        # validate user and password are valid
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
            raise DRFValidationError("Unable to create user.")
        return username

    def save(self):
        new_user = User.objects.create_user(
            username=self.validated_data['username'],
            password=self.validated_data['password'],
        )

        # Create our user profile at the same time
        UserProfile.objects.create(user=new_user)

        login(self.context.get('request'), new_user)


class ProfileSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    feed_is_public = serializers.BooleanField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        exclude = ('id', 'relations',)
        read_only_fields = ('following', 'relations',)

    def get_following(self, obj):

        if not self.context['request'].user or \
            not self.context['request'].user.is_authenticated:
            return False

        if self.context['request'].user.profile == self.instance:
            # We follow ourselves, of course.
            return True

        return self.context['request'].user.profile in self.instance.get_followers()


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
