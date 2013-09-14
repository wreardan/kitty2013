from django.db import models
from django.contrib.auth.models import User

class Meow(models.Model):
    text = models.CharField(max_length=160)
    user = models.ForeignKey(User)
    ts = models.DateTimeField(auto_now_add=True)
