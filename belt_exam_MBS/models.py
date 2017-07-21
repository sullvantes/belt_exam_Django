# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

class UserManager(models.Manager):
    def register_validator(self, user_input):
        errors = {}
        input_email = user_input['email']
        check_email_list = User.objects.filter(email = input_email)
        if len(check_email_list) <> 0:
            errors['existing'] = 'This email is already registered. Log in.'
        if len(user_input['first_name']) < 2:
            errors['first_name'] = 'First name must be at least 2 characters long'
        if not (user_input['first_name']).isalpha() or not (user_input['last_name']).isalpha():
            errors['name_chars'] = 'Name fields can only contain letters of the alphabet'
        if len(user_input['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters long'
        if user_input['password'] != user_input['confirm']:
            errors['confirm_pw'] = 'Passwords do not match. Try again.'
        if len(user_input['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters long'
        if not EMAIL_REGEX.match(user_input['email']):
            errors['email'] = 'Email syntax not valid'
        return errors 
    def login_validator(self, user_input):
        errors = {}
        input_email = user_input['email']
        password=user_input['password']
        this_user=User.objects.get(email=input_email)
        if not bcrypt.checkpw(password.encode(), this_user.password.encode()):
            errors['password'] = 'Incorrect Password'
        return errors 


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects=UserManager()

