import graphene
from graphene_django.forms.mutation import DjangoModelFormMutation

from django import forms

from .models import Workshop, Lesson, Slide, Direction


# adds an __init__ to a form class that sets every field to not be required
def no_required(cls):
    def __init__(self, *args, **kwargs):
        super(cls, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

    setattr(cls, "__init__", __init__)
    return cls


# Workshop


class CreateWorkshopForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = ['name', 'description', 'author']


class CreateWorkshop(DjangoModelFormMutation):
    class Meta:
        form_class = CreateWorkshopForm


@no_required
class EditWorkshopForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = ['description']


class EditWorkshop(DjangoModelFormMutation):
    class Meta:
        form_class = EditWorkshopForm


# Lesson


class CreateLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['name', 'description', 'workshop']


class CreateLesson(DjangoModelFormMutation):
    class Meta:
        form_class = CreateLessonForm


@no_required
class EditLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['name', 'description']


class EditLesson(DjangoModelFormMutation):
    class Meta:
        form_class = EditLessonForm


# Slide


class CreateSlideForm(forms.ModelForm):
    class Meta:
        model = Slide
        fields = ['name', 'description', 'lesson']


class CreateSlide(DjangoModelFormMutation):
    class Meta:
        form_class = CreateSlideForm


@no_required
class EditSlideForm(forms.ModelForm):
    class Meta:
        model = Slide
        fields = ['name', 'description']


class EditSlide(DjangoModelFormMutation):
    class Meta:
        form_class = EditSlideForm


class Mutation(graphene.ObjectType):
    create_workshop = CreateWorkshop.Field()
    edit_workshop = EditWorkshop.Field()

    create_lesson = CreateLesson.Field()
    edit_lesson = EditLesson.Field()

    create_slide = CreateSlide.Field()
    edit_slide = EditSlide.Field()
