from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from keyTracker.forms import *
from keyTracker.models import Key

# Create your views here.


def is_member(user, group):
    # check membership of a user in a group
    return user.groups.filter(name=group).exists()


def homepage(request):
    # if user is not logged in, show login page
    if not request.user.is_authenticated:
        print("not logged in")
        return redirect('keyTracker:login')
    # user should be part of DI group, so not everyone can see who has the key
    if not is_member(user=request.user, group='DI'):
        return HttpResponse("Awaiting account validation")

    # get the last key entry from the database
    lastKey = Key.objects.latest('time')

    if request.method == "POST":
        form = UpdateKeyForm(request.POST)
        if form.is_valid():
            # KEY TAKEN
            if "taken" in request.POST:
                if lastKey.keyHolder_id is request.user.id:
                    print(
                        f"user {request.user.username} tried to take a key they already have")
                # create a new key and set the keyHolder to the current user, set isReturned to False
                key = Key(keyHolder=request.user, isReturned=False)
                key.save()
                return redirect("keyTracker:homepage")
            # KEY RETURNED
            if "returned" in request.POST:
                # check if the user has the key
                if not lastKey.isReturned and lastKey.keyHolder_id is request.user.id:
                    key = Key(keyHolder=request.user, isReturned=True)
                    key.save()
                else:
                    print(
                        f"User {request.user} tried to return a key they don't have")

    # if method is GET
    updateKeyForm = UpdateKeyForm(data=request.POST)
    return render(request=request,
                  template_name='keyTracker/homepage.html',
                  context={"updateKeyForm": updateKeyForm,
                           "lastKey": lastKey,
                           })


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("keyTracker:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request=request,
                          template_name="keyTracker/register.html",
                          context={"form": form})

    # elif request.method == "GET":
    form = NewUserForm()
    return render(request=request,
                  template_name="keyTracker/register.html",
                  context={"form": form}
                  )


def login_request(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('keyTracker:homepage')

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('keyTracker:homepage')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="keyTracker/login.html",
                  context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")  # TODO messages
    return redirect("keyTracker:homepage")


def history(request):
    if request.user.is_authenticated and is_member(user=request.user, group='DI'):
        # get all keys from the database
        keys = Key.objects.all().order_by('-time')[:12]
        # TODO: filter to only show n amount of keys (lazy load more)
        return render(request=request,
                      template_name='keyTracker/history.html',
                      context={"keys": keys})
    else:
        return redirect('keyTracker:login')
