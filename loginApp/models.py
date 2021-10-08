from django.db import models
import re
import bcrypt
from .models import *

# Create your models here.
class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name must be at least 2 characters; letters only"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name must be at least 2 characters; letters only"
        if len(postData['password']) < 8:
            errors["password"] = "Password must be at least 8 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email_address']):         
            errors['email_address'] = ("Invalid Email Address")
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Passwords do not match"
        if len(User.objects.filter(email_address=postData['email_address'])) > 0:
            errors['email_address_exists'] = "That email address is already registered to another user"
        return errors
    def login_validator(self, postData):
        errors = {}
        LoginUser = User.objects.filter(email_address=postData['log_email_address'])
        if len(LoginUser) > 0:
            if bcrypt.checkpw(postData['log_password'].encode(), LoginUser[0].password.encode()):
                print('Password Matches')
            else:
                errors['log_password'] = "Email address and password combination is incorrect"
        else:
            errors['log_email_address'] = "There is no account associated with that Email Address"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email_address = models.CharField(max_length=60)
    password = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return '{}'.format(self.first_name)
