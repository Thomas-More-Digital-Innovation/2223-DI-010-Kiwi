from django import forms
from django.db import models
from django.contrib.auth.models import User


class UpdateKeyForm(forms.Form):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.TextField(max_length=500, blank=True)
