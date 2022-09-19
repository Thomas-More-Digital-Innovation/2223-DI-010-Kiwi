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


def homepage(request):
    # if logged in, redirect to login page
    if request.user.is_authenticated:
        if request.method == "POST":
            form = UpdateKeyForm(request.POST)
            if form.is_valid():
                if "taken" in request.POST:
                    # create a new key and set the keyHolder to the current user, set isReturned to False
                    key = Key(keyHolder=request.user, isReturned=False)
                    key.save()
                    return redirect("keyTracker:homepage")
                if "returned" in request.POST:
                    # TODO: check if the user has the key before they can return it
                    # The key is returned, set the keyHolder to None and isReturned to True
                    key = Key(keyHolder=None, isReturned=True)
                    key.save()

        # get the latest created key entry from the database
        lastKey = Key.objects.latest('time')
        # get the name of the latest key holder
        lastKeyHolder = lastKey.keyHolder
        updateKeyForm = UpdateKeyForm(data=request.POST)
        return render(request=request,
                      template_name='keyTracker/homepage.html',
                      context={"updateKeyForm": updateKeyForm, "lastKeyHolder": lastKeyHolder})
     # if not logged in, redirect to login page
    else:
        return redirect('keyTracker:login')


def register(request):
    if request.method == "POST":
        print("POST")
        form = UserCreationForm(request.POST)
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
                          template_name="register",
                          context={"form": form})

    # elif request.method == "GET":
    form = UserCreationForm
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
    # get all keys from the database
    keys = Key.objects.all()
    return render(request=request,
                  template_name='keyTracker/history.html',
                  context={"keys": keys})
