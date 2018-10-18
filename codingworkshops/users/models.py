from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import ASCIIUsernameValidator

RESERVED_USERNAMES = ['enter', 'signup', 'about']


class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(
            self.model.USERNAME_FIELD
        )
        return self.get(**{case_insensitive_username_field: username})


def username_validator(username):
    return username not in RESERVED_USERNAMES


class User(AbstractUser):
    objects = CustomUserManager()

    username_validators = [ASCIIUsernameValidator(), username_validator]

    bio = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
