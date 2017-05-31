# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Item, User
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
def index(request):
    if not "id" in request.session:
        return redirect("/")
    this_user = User.objects.get(id=request.session["id"])
    wishlist_items = this_user.wish.all()
    all_items = Item.objects.all()
    others_items = []
    for item in all_items:
        status = True
        for thing in wishlist_items:
            if item == thing: #if item.added_by == thing.added_by:
                status = False
        if status:
            others_items.append(item)
    print others_items
    context = {
        "others_items": others_items,
        "wishlist_items": wishlist_items,
    }
    return render(request, "wishlist/index.html", context)

def addpage(request):
    if not "id" in request.session:
        return redirect("/")
    return render(request, "wishlist/addpage.html")

def makeitem(request):
    if request.method == "POST":
        response = Item.objects.additem(request.POST, request.session["user"])
        if response["status"]:
            return redirect("/wishlist")
        else:
            for error in response["errors"]:
                messages.error(request, error)
    return redirect("/wishlist/create")

def item(request, id):
    if not "id" in request.session:
        return redirect("/")
    item = Item.objects.get(id=id)
    item_users = item.wishlist.all()
    context = {
        "item": item,
        "item_users": item_users,
    }
    return render(request, "wishlist/item.html", context)

def additem(request, id):
    if not "id" in request.session:
        return redirect("/")
    Item.objects.itemtowishlist(id, request.session["id"])
    return redirect("/wishlist")

def deleteitem(request, itemid):
    if not "id" in request.session:
        return redirect("/")
    Item.objects.deleteitem(itemid)
    return redirect("/wishlist")

def removefromlist(request, itemid):
    if not "id" in request.session:
        return redirect("/")
    Item.objects.removefromlist(itemid, request.session["id"])
    return redirect("/wishlist")
