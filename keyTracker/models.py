from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.


class Key(models.Model):
    keyHolder = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    isReturned = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now_add=True)

    def status(self):
        if self.isReturned == True:
            return "The key is Returned"
        else:
            return f"{self.keyHolder} has the key"
