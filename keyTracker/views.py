from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Group, User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from keyTracker.forms import *
from keyTracker.models import Key

# Create your views here.


def is_member(user, group):
    # check membership of a user in a group
    return user.groups.filter(name=group).exists()


def homepage(request):
    # if user is not logged in, show login page
    if not request.user.is_authenticated:
        return redirect('keyTracker:login')
    # user should be part of DI group, so not everyone can see who has the key
    if not is_member(user=request.user, group='DI'):
        return render(request=request,
                      template_name='keyTracker/pending.html')

    # get the last key entry from the database
    lastKey = Key.objects.latest('time')

    if request.method == "POST":
        form = UpdateKeyForm(request.POST)
        if form.is_valid():
            # KEY TAKEN
            if "taken" in request.POST:
                if lastKey.keyHolder_id is request.user.id:
                    print(
                        f"user {request.user.username} tried to take a key they already have")  # TODO: convert to msg
                    return redirect("keyTracker:homepage")
                # create a new key and set the keyHolder to the current user, set isReturned to False
                key = Key(keyHolder=request.user, isReturned=False)
                key.save()
                return redirect("keyTracker:homepage")
            # KEY RETURNED
            if "returned" in request.POST:
                # check if the user has the key
                if not lastKey.isReturned and lastKey.keyHolder_id is request.user.id:
                    # key = Key(keyHolder=request.user, isReturned=True)
                    key = Key(keyHolder=None, isReturned=True)
                    key.save()
                else:
                    print(
                        f"User {request.user} tried to return a key they don't have")  # TODO: convert to msg
                return redirect("keyTracker:homepage")

    # if method is GET
    updateKeyForm = UpdateKeyForm(data=request.POST)
    return render(request=request,
                  template_name='keyTracker/homepage.html',
                  context={"updateKeyForm": updateKeyForm,
                           "lastKey": lastKey,
                           })


def login_request(request):
    if request.user.is_authenticated:
        # if already logged in, redirect to homepage
        messages.info(request, "You are already logged in.")
        return redirect('keyTracker:homepage')
    return render(request=request, template_name="keyTracker/login.html",)


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")  # TODO messages
    return redirect("keyTracker:homepage")  # TODO redirect to login page


def history(request):
    if request.user.is_authenticated and is_member(user=request.user, group='DI'):
        # get all keys from the database
        keys = Key.objects.all().order_by('-time')[:12]
        # TODO: filter to only show n amount of keys (lazy load more)
        return render(request=request,
                      template_name='keyTracker/history.html',
                      context={"keys": keys})
    else:
        return redirect('keyTracker:homepage')


@login_required
@user_passes_test(lambda u: u.is_staff)
def remove_user(request):
    if request.method == "POST":
        form = UserRemovalForm(request.POST)
        if form.is_valid():
            if "remove_btn" in request.POST:
                user = User.objects.get(username=request.POST['current_user'])
                user.delete()
                return redirect("keyTracker:dashboard")
    return redirect("keyTracker:dashboard")


@login_required
@user_passes_test(lambda u: u.is_staff)
def review_application(request):
    if request.method == "POST":
        form = UserAcceptanceForm(request.POST)
        if form.is_valid():
            verdict = form.cleaned_data.get("verdict")
            pending_user = form.cleaned_data.get("pending_user")
            if verdict == "accept":
                user = User.objects.get(username=pending_user)
                user.groups.add(Group.objects.get(name='DI'))
                user.save()
                messages.info(
                    request, f"User {pending_user} has been accepted")
            elif verdict == "deny":
                user = User.objects.get(username=pending_user)
                user.delete()
                messages.info(
                    request, f"User {pending_user} has been denied")
            else:
                messages.info(request, "Something went wrong")
        return redirect('keyTracker:dashboard')


@login_required
@user_passes_test(lambda u: u.is_staff)
def dashboard(request):
    # get all users that are in the DI group
    current_users = User.objects.filter(groups__name='DI')
    # get all users that are not in the DI group
    pending_users = User.objects.exclude(groups__name='DI')
    return render(request=request,
                  template_name='keyTracker/dashboard.html',
                  context={"current_users": current_users,
                           "pending_users": pending_users})
