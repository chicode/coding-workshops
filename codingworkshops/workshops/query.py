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
        WorkshopType, workshop=graphene.String(required=True)
    )

    def resolve_all_workshops(self, info):
        return Workshop.objects.all()

    def resolve_workshop(self, info, workshop):
        return Workshop.objects.get(name=workshop)

    lesson = graphene.Field(
        LessonType,
        workshop=graphene.String(required=True),
        lesson=graphene.ID(required=True),
    )

    def resolve_lesson(self, info, workshop, lesson):
        try:
            return Lesson.objects.get(workshop__name=workshop, id=lesson)
        except ObjectDoesNotExist:
            return None

    slide = graphene.Field(
        SlideType,
        workshop=graphene.String(required=True),
        lesson=graphene.ID(required=True),
        slide=graphene.ID(required=True)
    )

    def resolve_slide(self, info, workshop, lesson, slide):
        try:
            return Slide.objects.get(
                lesson__workshop__name=workshop, lesson__id=lesson, id=slide
            )
        except ObjectDoesNotExist:
            return None
