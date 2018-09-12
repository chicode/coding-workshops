from django.db import models
from codingworkshops.users.models import User


class Workshop(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)


class Slide(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    starting_code = models.TextField(default='')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)


class Direction(models.Model):
    description = models.CharField(max_length=500)
    hint = models.CharField(max_length=50)
    slide = models.ForeignKey(Slide, on_delete=models.CASCADE)
