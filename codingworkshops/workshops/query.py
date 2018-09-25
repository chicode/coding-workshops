import graphene
import graphene_django.types

from django.core.exceptions import ObjectDoesNotExist

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

    def resolve_all_workshops(self, info):
        return Workshop.objects.all()

    @protect
    def resolve_workshop(self, info, human, workshop):
        return Workshop.objects.get(
            author=User.objects.get(username=human), name=workshop
        )

    lesson = graphene.Field(
        LessonType,
        human=graphene.String(required=True),
        workshop=graphene.String(required=True),
        lesson=graphene.ID(required=True),
    )

    @protect
    def resolve_lesson(self, info, human, workshop, lesson):
        return Lesson.objects.get(
            workshop__author=User.objects.get(username=human),
            workshop__name=workshop,
            id=lesson
        )

    slide = graphene.Field(
        SlideType,
        human=graphene.String(required=True),
        workshop=graphene.String(required=True),
        lesson=graphene.ID(required=True),
        slide=graphene.ID(required=True)
    )

    @protect
    def resolve_slide(self, info, human, workshop, lesson, slide):
        return Slide.objects.get(
            lesson__workshop__author=User.objects.get(username=human),
            lesson__workshop__name=workshop,
            lesson__id=lesson,
            id=slide
        )
