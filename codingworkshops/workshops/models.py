from django.db import models


class Workshop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name
