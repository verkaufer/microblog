from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# In case we want to switch out our auth user model in the future
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

FOLLOWING = 1
RELATION_TYPES = (
    (FOLLOWING, "Following"),
)

# Create your models here.
class UserProfile(models.Model):

    user = models.OneToOneField(AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    feed_is_public = models.BooleanField(default=True)
    relations = models.ManyToManyField("self", through="Relation", symmetrical=False, related_name="related")

    def get_following(self):
        return self.relations.filter(to_user__initiator=self, to_user__relation_type=FOLLOWING)

    def get_followers(self):
        return self.related.filter(from_user__receiver=self, from_user__relation_type=FOLLOWING)

    def add_relation(self, userprofile, relationship_type):
        """
        Creates new relation of type relationship_type.
        Custom method needed because of ManyToMany w/intermediate table
        """
        relation, created = Relation.objects.get_or_create(
            initiator=self,
            receiver=userprofile,
            relation_type=relationship_type
        )
        return relation

    def remove_relation(self, userprofile, relationship_type):
        """
        Removes relation with userprofile of type relationship_type.
        Custom method needed because of ManyToMany w/intermediate table
        """
        Relation.objects.filter(
            initiator=self,
            receiver=userprofile,
            relation_type=relationship_type
        ).delete()


class Relation(models.Model):

    initiator = models.ForeignKey(UserProfile, related_name="from_user", on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name="to_user", on_delete=models.CASCADE)
    relation_type = models.IntegerField(choices=RELATION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)     

    class Meta:
        unique_together = ("initiator", "receiver", "relation_type")