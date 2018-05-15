from django.db import models
from django.conf import settings

from accounts.models import FOLLOWING

# In case we want to switch out our auth user model in the future
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

# Create your models here.

class FollowedUsersQuerySet(models.QuerySet):

    def from_authors_followed_by_user(self, for_user):
        return self.filter(author__profile__in=for_user.profile.get_following())


class Post(models.Model):

    author = models.ForeignKey(AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = FollowedUsersQuerySet.as_manager()
