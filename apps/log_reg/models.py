# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import bcrypt


class UserManager(models.Manager):
    #Function for validation of registration form database
    #If validation is OK then add user to database
    #If invalid then return error messages
    #########################################
    #return if form data valid, error messages
    def registration(self, postdata):
    # making an error list to store error messages if fields are not valid
        errors = []
    #checking input fields for proper completion
        if len(postdata["name"]) < 4:
            errors.append("please enter a name of at least 4 charicters")
        if len(postdata["username"]) < 4:
            errors.append("please enter a username of at least 4 charicters")
        if self.filter(user_name=postdata["username"]):
            errors.append("that username is already in use")
        if len(postdata["password"]) < 8:
            errors.append("your password must be 8 charicters long")
        if postdata["password"] != postdata["confirmpassword"]:
            errors.append("your passwords must match")
    #checking if there were any errors and acting accordingly
    #creating response dictionary to return all relevent data to views
        response = {}
        if errors:
            response["status"] = False
            response["errors"] = errors
        else:
            response["status"] = True
            hashed = bcrypt.hashpw(postdata["password"].encode('utf-8'), bcrypt.gensalt())
            response["user"] = self.create(first_name=postdata["name"], user_name=postdata["username"], password=hashed, date_hired=postdata["date"])
        return response

    def login(self, postdata):
        errors = []
        response = {}
        if len(postdata["username"]) < 4 or len(postdata["password"]) < 8:
            errors.append("please enter in a valid username and password")
            response["status"] = False
            response["errors"] = errors
            return response
        user = self.filter(user_name=postdata["username"])
        if user:
            print "found"
            for item in user:
                password = postdata["password"]
                if bcrypt.hashpw(password.encode('utf-8'), item.password.encode('utf-8')) == item.password.encode('utf-8'):
                    response["status"] = True
                    response["user"] = user
                else:
                    errors.append("invalid password")
                    response["status"] = False
        else:
            response["status"] = False
            errors.append("username not found")

        response["errors"] = errors
        return response

class User(models.Model):
    first_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    date_hired = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.first_name

    objects = UserManager()
