from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator

RESERVED_USERNAMES = ['enter', 'signup', 'about']


def username_validator(username):
    return username not in RESERVED_USERNAMES


class User(AbstractUser):
    username_validators = [ASCIIUsernameValidator(), username_validator]

    bio = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
