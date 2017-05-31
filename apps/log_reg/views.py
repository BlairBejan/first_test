# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import User
from django.shortcuts import render, redirect
from django.contrib import messages

def index(request):
    return render(request, "log_reg/index.html")

def register(request):
    if request.method == "POST":
        response = User.objects.registration(request.POST)
        if response["status"]:
            messages.error(request, "Account created, proceed to login")
        else:
            for error in response["errors"]:
                messages.error(request, error)
    return redirect("/")

def login(request):
    if request.method == "POST":
        response = User.objects.login(request.POST)
        if response["status"]:
            for user in response["user"]:
                request.session["user"] = user.user_name
                request.session["id"] = user.id
        #change to index of first app
                return redirect("/wishlist")
        else:
            for error in response["errors"]:
                messages.error(request, error)
    return redirect("/")

def logout(request):
    request.session.flush()
    return redirect("/")
