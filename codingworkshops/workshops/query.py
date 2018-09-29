from django.core.exceptions import ObjectDoesNotExist

import graphene
import graphene_django.types

from .models import Workshop, Lesson, Slide, Direction
from codingworkshops.users.models import User


def protect(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ObjectDoesNotExist:
            return None

    return wrapper


class WorkshopType(graphene_django.types.DjangoObjectType):
    class Meta:
        model = Workshop


class LessonType(graphene_django.types.DjangoObjectType):
    class Meta:
        model = Lesson


class SlideType(graphene_django.types.DjangoObjectType):
    class Meta:
        model = Slide


class DirectionType(graphene_django.types.DjangoObjectType):
    class Meta:
        model = Direction


class Query(graphene.ObjectType):
    all_workshops = graphene.List(WorkshopType)
    workshop = graphene.Field(
        WorkshopType,
        human=graphene.String(required=True),
        workshop=graphene.String(required=True)
    )
    user_workshops = graphene.List(
        WorkshopType,
        human=graphene.String(required=True),
    )

    def resolve_all_workshops(self, info):
        return Workshop.objects.all()

    def resolve_workshop(self, info, human, workshop):
        return Workshop.objects.get(
            author=User.objects.get(username=human), slug=workshop
        )

    def resolve_user_workshops(self, info, human):
        return Workshop.objects.filter(author=User.objects.get(username=human))

    lesson = graphene.Field(
        LessonType,
        human=graphene.String(required=True),
        workshop=graphene.String(required=True),
        lesson=graphene.Int(required=True),
    )
    workshop_lessons = graphene.List(
        LessonType,
        human=graphene.String(required=True),
        workshop=graphene.String(required=True),
    )

    def resolve_lesson(self, info, human, workshop, lesson):
        return Lesson.objects.get(
            workshop__author=User.objects.get(username=human),
            workshop__slug=workshop,
            index=lesson
        )

    def resolve_workshop_lessons(self, info, human, workshop):
        return Lesson.objects.filter(
            workshop__author=User.objects.get(username=human),
            workshop__slug=workshop,
        )

    slide = graphene.Field(
        SlideType,
        human=graphene.String(required=True),
        workshop=graphene.String(required=True),
        lesson=graphene.Int(required=True),
        slide=graphene.Int(required=True)
    )
    lesson_slides = graphene.List(
        SlideType,
        human=graphene.String(required=True),
        workshop=graphene.String(required=True),
        lesson=graphene.Int(required=True),
    )

    def resolve_slide(self, info, human, workshop, lesson, slide):
        return Slide.objects.get(
            lesson__workshop__author=User.objects.get(username=human),
            lesson__workshop__slug=workshop,
            lesson__index=lesson,
            index=slide
        )

    def resolve_lesson_slides(self, info, human, workshop, lesson):
        return Slide.objects.filter(
            lesson__workshop__author=User.objects.get(username=human),
            lesson__workshop__slug=workshop,
            lesson__index=lesson
        )
