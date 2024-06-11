from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    friend_list = models.CharField(max_length=1000,default="")
    request_received = models.CharField(max_length=1000,default="")
    request_sent = models.CharField(max_length=1000,default="")

    def __str__(self):
        return self.user.username