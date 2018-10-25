from django.db import models
from codingworkshops.users.models import User
from django.utils.text import slugify

RESERVED_WORKSHOP_NAMES = ['edit']


def name_validator(name):
    return name not in RESERVED_WORKSHOP_NAMES


class Workshop(models.Model):
    class Meta:
        ordering = ['pk']
        unique_together = ('author', 'name')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    name = models.CharField(max_length=50, validators=[name_validator])
    slug = models.SlugField(max_length=50, blank=True)
    description = models.CharField(max_length=500, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_draft = models.BooleanField()
    contributors = models.ManyToManyField(
        User, related_name='contributed_workshop_set'
    )
    source_url = models.URLField(max_length=300, blank=True)


class Lesson(models.Model):
    class Meta:
        ordering = ['index']
        unique_together = ('workshop', 'index')

    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)

    index = models.IntegerField()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)


class Slide(models.Model):
    class Meta:
        ordering = ['index']
        unique_together = ('lesson', 'index')

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    index = models.IntegerField()
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    starting_code = models.TextField(blank=True)


class Direction(models.Model):
    class Meta:
        ordering = ['index']
        unique_together = ('slide', 'index')

    slide = models.ForeignKey(Slide, on_delete=models.CASCADE)

    index = models.IntegerField()
    description = models.TextField()
    hint = models.CharField(max_length=50, blank=True)
