from django.db import models
from codingworkshops.users.models import User


class Workshop(models.Model):
    class Meta:
        ordering = ['pk']

    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Lesson(models.Model):
    class Meta:
        ordering = ['pk']

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)


class Slide(models.Model):
    class Meta:
        ordering = ['pk']

    name = models.CharField(max_length=50)
    description = models.TextField()
    starting_code = models.TextField(default='')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)


class Direction(models.Model):
    description = models.TextField()
    hint = models.CharField(max_length=50, blank=True)
    slide = models.ForeignKey(Slide, on_delete=models.CASCADE)
