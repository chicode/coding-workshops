import graphene

from .models import Workshop, Lesson, Slide, Direction
from ..mutation_helpers import *

# Workshop


def workshop_verify(user, obj):
    return user == obj.author


class CreateWorkshop(ModelMutation, graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    @authenticated
    def mutate(self, info, **kwargs):
        obj = Workshop(
            is_draft=True,
            author=info.context.user,
            **kwargs,
        )
        return validate(obj)


class EditWorkshop(ModelMutation, graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

        description = graphene.String()

    @authenticated
    def mutate(self, info, **kwargs):
        obj = Workshop.objects.get(pk=kwargs.pop('pk'))
        verify_permission(info, workshop_verify, obj)
        update(obj, kwargs)
        return validate(obj)


class DeleteWorkshop(ModelMutation, graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

    @authenticated
    def mutate(self, info, **kwargs):
        obj = Workshop.objects.get(pk=kwargs.pop('pk'))
        verify_permission(info, workshop_verify, obj)
        return delete(obj)


# Lesson


def lesson_verify(user, obj):
    return user == obj.workshop.author


class CreateLesson(ModelMutation, graphene.Mutation):
    class Arguments:
        workshop = graphene.ID(required=True)

        name = graphene.String()

    @authenticated
    def mutate(self, info, **kwargs):
        workshop = Workshop.objects.get(pk=kwargs.pop('workshop'))
        if not kwargs.get('name'):
            kwargs['name'] = generate_unique_name(Lesson, workshop=workshop)
        obj = Lesson(
            workshop=workshop,
            index=Lesson.objects.filter(workshop=workshop).count() + 1,
            **kwargs,
        )
        verify_permission(info, lesson_verify, obj)
        return validate(obj)


class EditLesson(ModelMutation, graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

        name = graphene.String()
        description = graphene.String()

    @authenticated
    def mutate(self, info, **kwargs):
        obj = Lesson.objects.get(pk=kwargs.pop('pk'))
        verify_permission(info, lesson_verify, obj)
        update(obj, kwargs)
        return validate(obj)


class DeleteLesson(ModelMutation, graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

    @authenticated
    def mutate(self, info, **kwargs):
        obj = Lesson.objects.get(pk=kwargs.pop('pk'))
        verify_permission(info, lesson_verify, obj)
        return delete_indexed(Lesson, obj)


class MoveLesson(ModelMutation, graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

        index = graphene.Int(required=True)

    @authenticated
    def mutate(self, info, **kwargs):
        obj = Lesson.objects.get(pk=kwargs.pop('pk'))
        verify_permission(info, lesson_verify, obj)
        return move(
            Lesson, {'workshop__pk': obj.workshop.pk}, obj,
            kwargs.get('index')
        )


# Slide


def slide_verify(user, obj):
    return user == obj.lesson.workshop.author


class CreateSlide(ModelMutation, graphene.Mutation):
    class Arguments:
        lesson = graphene.ID(required=True)

        name = graphene.String()

    @authenticated
    def mutate(self, info, **kwargs):
        lesson = Lesson.objects.get(pk=kwargs.pop('lesson'))
        if not kwargs.get('name'):
            kwargs['name'] = generate_unique_name(Slide, lesson=lesson)
        obj = Slide(
            lesson=lesson,
            index=Slide.objects.filter(lesson=lesson).count() + 1,
            **kwargs,
        )
        verify_permission(info, slide_verify, obj)
        return validate(obj)


class EditSlide(ModelMutation, graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

        name = graphene.String()
        description = graphene.String()
        starting_code = graphene.String()

    @authenticated
    def mutate(self, info, **kwargs):
        obj = Slide.objects.get(pk=kwargs.pop('pk'))
        verify_permission(info, slide_verify, obj)
        update(obj, kwargs)
        return validate(obj)


class DeleteSlide(ModelMutation, graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

    @authenticated
    def mutate(self, info, **kwargs):
        obj = Slide.objects.get(pk=kwargs.pop('pk'))
        verify_permission(info, slide_verify, obj)
        return delete_indexed(Slide, obj)


class MoveSlide(ModelMutation, graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

        index = graphene.Int(required=True)

    @authenticated
    def mutate(self, info, **kwargs):
        obj = Slide.objects.get(pk=kwargs.pop('pk'))
        verify_permission(info, slide_verify, obj)
        return move(
            Slide, {'lesson__pk': obj.lesson.pk}, obj, kwargs.get('index')
        )


# Direction


def direction_verify(user, obj):
    return user == obj.slide.lesson.workshop.author


class CreateDirection(ModelMutation, graphene.Mutation):
    class Arguments:
        slide = graphene.ID(required=True)

        description = graphene.String(required=True)

    @authenticated
    def mutate(self, info, **kwargs):
        slide = Slide.objects.get(pk=kwargs.pop('slide'))
        obj = Direction(
            slide=slide,
            index=Direction.objects.filter(slide=slide).count() + 1,
            **kwargs,
        )
        verify_permission(info, direction_verify, obj)
        return validate(obj)


class EditDirection(ModelMutation, graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

        index = graphene.Int()
        description = graphene.String()
        hint = graphene.String()

    @authenticated
    def mutate(self, info, **kwargs):
        obj = Direction.objects.get(pk=kwargs.pop('pk'))
        verify_permission(info, direction_verify, obj)
        update(obj, kwargs)
        return validate(obj)


class DeleteDirection(ModelMutation, graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

    @authenticated
    def mutate(self, info, **kwargs):
        obj = Direction.objects.get(pk=kwargs.pop('pk'))
        verify_permission(info, direction_verify, obj)
        return delete_indexed(Direction, obj)


class MoveDirection(ModelMutation, graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

        index = graphene.Int(required=True)

    @authenticated
    def mutate(self, info, **kwargs):
        obj = Direction.objects.get(pk=kwargs.pop('pk'))
        verify_permission(info, direction_verify, obj)
        return move(
            Direction, {'slide__pk': obj.slide.pk}, obj, kwargs.get('index')
        )


# Top-level


class Mutation(graphene.ObjectType):
    create_workshop = CreateWorkshop.Field()
    edit_workshop = EditWorkshop.Field()
    delete_workshop = DeleteWorkshop.Field()

    create_lesson = CreateLesson.Field()
    edit_lesson = EditLesson.Field()
    delete_lesson = DeleteLesson.Field()
    move_lesson = MoveLesson.Field()

    create_slide = CreateSlide.Field()
    edit_slide = EditSlide.Field()
    delete_slide = DeleteSlide.Field()
    move_slide = MoveSlide.Field()

    create_direction = CreateDirection.Field()
    edit_direction = EditDirection.Field()
    delete_direction = DeleteDirection.Field()
    move_direction = MoveDirection.Field()
