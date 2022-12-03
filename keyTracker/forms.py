from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UpdateKeyForm(forms.Form):
    pass


class UserAcceptanceForm(forms.Form):
    verdict = forms.CharField()
    pending_user = forms.CharField(widget=forms.HiddenInput())


class UserRemovalForm(forms.Form):
    current_user = forms.CharField(widget=forms.HiddenInput())
    remove_btn = forms.CharField()
