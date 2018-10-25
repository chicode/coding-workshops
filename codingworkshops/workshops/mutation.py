from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

import requests
import requests.exceptions
from ruamel.yaml import YAML

import graphene

from .models import Workshop, Lesson, Slide, Direction
from codingworkshops.users.models import User
from ..mutation_helpers import *

# Workshop


def workshop_verify(user, obj):
    return user == obj.author or user in obj.contributors.all()


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
        contributors = graphene.List(graphene.NonNull(graphene.String))
        source_url = graphene.String()

    @authenticated
    def mutate(self, info, **kwargs):
        obj = Workshop.objects.get(pk=kwargs.pop('pk'))
        verify_permission(info, workshop_verify, obj)

        if kwargs.get('contributors'):
            # only the author can modify contributors
            if info.context.user == obj.author:
                for contributor in kwargs.get('contributors'):
                    try:
                        User.objects.get(username=contributor)
                    except ObjectDoesNotExist:
                        return create_error(
                            field='contributors',
                            message='username does not exist'
                        )

                    if contributor == obj.author.username:
                        return create_error(
                            field='contributors',
                            message='you cannot add yourself as a contributor'
                        )
                    elif contributor in obj.contributors.values_list(
                        'username', flat=True
                    ):
                        return create_error(
                            field='contributors',
                            message='contributor already exists'
                        )

                obj.contributors.set(
                    User.objects.filter(
                        username__in=kwargs.pop('contributors')
                    )
                )
            else:
                # get rid of argument
                kwargs.pop('contributors')

        print(kwargs)

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


class SyncWorkshop(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

    ok = graphene.Boolean(required=True)
    error = graphene.String()

    @authenticated
    def mutate(self, info, **kwargs):
        obj = Workshop.objects.get(pk=kwargs.pop('pk'))
        verify_permission(info, workshop_verify, obj)

        try:
            with transaction.atomic():
                r = requests.get(obj.source_url)
                yaml = YAML(typ='safe')

                Direction.objects.filter(slide__lesson__workshop=obj).delete()
                Slide.objects.filter(lesson__workshop=obj).delete()
                Lesson.objects.filter(workshop=obj).delete()

                workshop = yaml.load(r.text)

                obj.name = workshop['name']
                obj.description = workshop.get('description', '')
                obj.save()

                for lesson_index, lesson in enumerate(workshop['lessons']):
                    lesson_obj = Lesson.objects.create(
                        name=lesson['name'],
                        description=lesson.get('description', ''),
                        index=lesson_index + 1,
                        workshop=obj,
                    )
                    for slide_index, slide in enumerate(
                        lesson.get('slides', [])
                    ):
                        slide_obj = Slide.objects.create(
                            name=slide['name'],
                            description=slide.get('description', ''),
                            index=slide_index + 1,
                            lesson=lesson_obj
                        )
                        for direction_index, direction in enumerate(
                            slide.get('directions', [])
                        ):
                            Direction.objects.create(
                                description=direction,
                                index=direction_index + 1,
                                slide=slide_obj
                            )

        except requests.exceptions.RequestException as e:
            print(e)
            return SyncWorkshop(
                ok=False, error="Couldn't complete the request"
            )

        return SyncWorkshop(ok=True)


# Lesson


def lesson_verify(user, obj):
    return user == obj.workshop.author or user in obj.workshop.contributors.all(
    )


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
    return user == obj.lesson.workshop.author or user in obj.lesson.workshop.contributors.all(
    )


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
    return user == obj.slide.lesson.workshop.author or user in obj.slide.lesson.workshop.contributors.all(
    )


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
    sync_workshop = SyncWorkshop.Field()

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
