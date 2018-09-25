import graphene

from .models import Workshop, Lesson, Slide, Direction
from ..mutation_helpers import *

# Workshop


class CreateWorkshop(ModelMutation, graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    @authenticated
    def mutate(self, info, **kwargs):
        workshop = Workshop(
            is_draft=True,
            author=info.context.user,
            **kwargs,
        )
        return validate(CreateWorkshop, workshop)


class EditWorkshop(ModelMutation, graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

        description = graphene.String()

    @authenticated
    def mutate(self, info, **kwargs):
        workshop = Workshop.objects.get(pk=kwargs.pop('pk'))
        if info.context.user != workshop.author:
            permission_denied()
        update(workshop, kwargs)
        return validate(EditWorkshop, workshop)


# Lesson


class CreateLesson(ModelMutation, graphene.Mutation):
    class Arguments:
        workshop = graphene.ID(required=True)

        index = graphene.Int(required=True)
        name = graphene.String(required=True)

    @authenticated
    def mutate(self, info, **kwargs):
        lesson = Lesson(
            workshop=Workshop.objects.get(pk=kwargs.pop('workshop')),
            **kwargs,
        )
        if info.context.user != lesson.workshop.author:
            permission_denied()
        return validate(CreateLesson, lesson)


class EditLesson(ModelMutation, graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

        name = graphene.String()
        description = graphene.String()

    @authenticated
    def mutate(self, info, **kwargs):
        lesson = Lesson.objects.get(pk=kwargs.pop('pk'))
        if info.context.user != lesson.workshop.author:
            permission_denied()
        update(lesson, kwargs)
        return validate(EditLesson, lesson)


# Slide


class CreateSlide(ModelMutation, graphene.Mutation):
    class Arguments:
        lesson = graphene.ID(required=True)

        index = graphene.Int(required=True)
        name = graphene.String(required=True)

    @authenticated
    def mutate(self, info, **kwargs):
        slide = Slide(
            lesson=Lesson.objects.get(pk=kwargs.pop('lesson')),
            **kwargs,
        )
        if info.context.user != slide.lesson.workshop.author:
            permission_denied()
        return validate(CreateSlide, slide)


class EditSlide(ModelMutation, graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

        name = graphene.String()
        description = graphene.String()
        starting_code = graphene.String()

    @authenticated
    def mutate(self, info, **kwargs):
        slide = Slide.objects.get(pk=kwargs.pop('pk'))
        if info.context.user != slide.lesson.workshop.author:
            permission_denied()
        update(slide, kwargs)
        return validate(EditSlide, slide)


# Direction


class CreateDirection(ModelMutation, graphene.Mutation):
    class Arguments:
        slide = graphene.ID(required=True)

        index = graphene.Int(required=True)
        description = graphene.String(required=True)

    @authenticated
    def mutate(self, info, **kwargs):
        direction = Direction(
            slide=Slide.objects.get(pk=kwargs.pop('slide')),
            **kwargs,
        )
        if info.context.user != direction.slide.lesson.workshop.author:
            permission_denied()
        return validate(CreateDirection, direction)


class EditDirection(ModelMutation, graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

        index = graphene.Int()
        description = graphene.String()
        hint = graphene.String()

    @authenticated
    def mutate(self, info, **kwargs):
        direction = Direction.objects.get(pk=kwargs.pop('pk'))
        if info.context.user != direction.slide.lesson.workshop.author:
            permission_denied()
        update(direction, kwargs)
        return validate(EditDirection, direction)


# Top-level


class Mutation(graphene.ObjectType):
    create_workshop = CreateWorkshop.Field()
    edit_workshop = EditWorkshop.Field()

    create_lesson = CreateLesson.Field()
    edit_lesson = EditLesson.Field()

    create_slide = CreateSlide.Field()
    edit_slide = EditSlide.Field()

    create_direction = CreateDirection.Field()
    edit_direction = EditDirection.Field()
