from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UpdateKeyForm(forms.Form):
    pass


# class NewUserForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     rnumber = forms.CharField(required=True, max_length=7)

#     class Meta:
#         model = User
#         fields = ("username", "email", "rnumber",
#                   "password1", "password2")

#         def save(self, commit=True):
#             user = super(NewUserForm, self).save(commit=False)
#             user.email = self.cleaned_data['email']
#             user.rnumber = self.cleaned_data['rnumber']
#             if commit:
#                 user.save()
#             return user
