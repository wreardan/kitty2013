from django.db import models
from django.contrib.auth.models import User

class Meow(models.Model):
    text = models.CharField(max_length=160)
    user = models.ForeignKey(User)
    ts = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField()

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    followers = models.ManyToManyField('self', symmetrical=False, blank=True)
    likes = models.ManyToManyField(Meow)
    cell_phone = models.BigIntegerField()
    tags = models.ManyToManyField(Meow, through='Tag', related_name="user_profile_tags")

class Tag(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    meow = models.ForeignKey(Meow)
    ts = models.DateTimeField(auto_now_add=True)
    x = models.PositiveIntegerField()
    y = models.PositiveIntegerField()