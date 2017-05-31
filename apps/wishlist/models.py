# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ..log_reg.models import User
from django.db import models


class ItemManager(models.Manager):
    def additem(self, postdata, username):
        errors = []
        response = {}
        if len(postdata["item"]) < 4:
            errors.append("entry must be greater than 4 charicters")
        if errors:
            response["status"] = False
            response["errors"] = errors
        else:
            this_item = self.create(product_name=postdata["item"], added_by=username)
            this_user = User.objects.get(user_name=username)
            this_item.wishlist.add(this_user)
            response["status"] = True
            response["item"] = this_item
        return response

    def itemtowishlist(self, item_id, user_id):
        this_item = self.get(id=item_id)
        this_user = User.objects.get(id=user_id)
        this_item.wishlist.add(this_user)
        return True

    def deleteitem(self, item_id):
        Item.objects.get(id=item_id).delete()
        return True

    def removefromlist(self, item_id, user_id):
        this_item = self.get(id=item_id)
        this_user = User.objects.get(id=user_id)
        this_item.wishlist.remove(this_user)
        return True

class Item(models.Model):
    product_name = models.CharField(max_length=50)
    added_by = models.CharField(max_length=50)
    wishlist = models.ManyToManyField(User, related_name="wish")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ItemManager()
