from django.db import models


class Workshop(models.Model):
    name = models.CharField(max_length=50, unique=True, primary_key=True)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)


class Slide(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)


class Direction(models.Model):
    description = models.CharField(max_length=500)
    hint = models.CharField(max_length=50)
    correct_code = models.TextField()
    slide = models.ForeignKey(Slide, on_delete=models.CASCADE)
