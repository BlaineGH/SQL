from __future__ import unicode_literals
from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]$')
NAME_REGEX = re.compile(r'^[a-zA-Z]$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 1:
            errors["first_name"] = "First name should be more than 1 characters"
        if len(postData['last_name']) < 1:
            errors["last_name"] = "Last name should be more than 1 characters"
        if len(postData['email']) < 1:
    		errors['"email'] = "Email is needed"
        if EMAIL_REGEX.match(postData['email']):
        	errors["email"] = "Not a valid Email"
        return errors

class User(models.Model):
	firstname = models.CharField(max_length=255)
	lastname = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now = True)	
	objects = UserManager()
		