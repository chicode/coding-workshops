import graphene
import graphene_django.types

from django.core.exceptions import ValidationError, ObjectDoesNotExist

from .models import Workshop, Lesson, Slide, Direction


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
        WorkshopType, name=graphene.String(required=True)
    )

    def resolve_all_workshops(self, info):
        return Workshop.objects.all()

    def resolve_workshop(self, info, name):
        return Workshop.objects.get(name=name)

    all_lessons = graphene.List(
        LessonType, workshop=graphene.String(required=True)
    )
    lesson = graphene.Field(
        LessonType,
        workshop_name=graphene.String(required=True),
        name=graphene.String(required=True),
    )

    def resolve_all_lessons(self, info, workshop):
        return Lesson.objects.get(workshop__name=workshop)

    def resolve_lesson(self, info, workshop, name):
        try:
            return Lesson.objects.get(workshop__name=workshop, name=name)
        except ObjectDoesNotExist:
            return None

    all_slides = graphene.List(
        SlideType,
        workshop=graphene.String(required=True),
        lesson=graphene.String(required=True),
    )
    slide = graphene.Field(
        SlideType,
        workshop=graphene.String(required=True),
        lesson=graphene.String(required=True),
        id=graphene.ID(required=True)
    )

    def resolve_all_slides(self, info, workshop, lesson):
        return Slide.objects.filter(
            lesson__workshop__name=workshop, lesson__name=lesson
        )

    def resolve_slide(self, info, workshop, lesson, id):
        try:
            return Slide.objects.get(
                workshop__name=workshop, lesson_name=lesson, id=id
            )
        except ObjectDoesNotExist:
            return None
