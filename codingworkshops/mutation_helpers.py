from django.core.exceptions import ValidationError
from django.db.models import F
from django.db import IntegrityError, transaction
import graphene


class ModelError(graphene.ObjectType):
    field = graphene.String(required=True)
    message = graphene.String(required=True)


class MutationResult(graphene.ObjectType):
    ok = graphene.Boolean(required=True)
    errors = graphene.List(ModelError)
    pk = graphene.ID()


class ModelMutation(graphene.ObjectType):
    Output = MutationResult


def create_errors(error_dict):
    return [
        ModelError(field=key, message=value[0])
        for key, value in error_dict.items()
    ]


def validate(model):
    try:
        model.full_clean()
    except ValidationError as e:
        return MutationResult(ok=False, errors=create_errors(e.message_dict))
    model.save()
    return MutationResult(ok=True, pk=model.pk)


def update(model, fields):
    for key, value in fields.items():
        setattr(model, key, value)


def delete(obj):
    obj.delete()
    return MutationResult(ok=True)


def delete_indexed(cls, initial_filters, obj):
    try:
        with transaction.atomic():
            obj.delete()

            # see the move function for the reason behind this mess
            # TODO fix this redundant code
            objs = cls.objects.filter(**initial_filters, index__gt=obj.index)
            pks = list(objs.values_list('pk', flat=True))
            objs = cls.objects.filter(pk__in=pks)

            objs.update(index=F('index') * -1)
            objs.update(index=F('index') * -1 - 1)

    except IntegrityError:
        index = 1
        for obj in cls.objects.filter(**initial_filters):
            obj.index = index
            obj.save()
            index += 1

    return MutationResult(ok=True)


def move(cls, initial_filters, obj, index):
    try:
        # atomic transaction necessary because they may still go wrong
        with transaction.atomic():
            # change the id to avoid uniqueness violation error
            old_index = obj.index
            if old_index == index:
                return

            # 0 is the reserved index for temp values
            obj.index = 0
            obj.save()

            objs = None
            if old_index < index:
                objs = cls.objects.filter(
                    **initial_filters, index__gt=old_index, index__lte=index
                )
            elif old_index > index:
                objs = cls.objects.filter(
                    **initial_filters, index__gte=index, index__lt=old_index
                )
            # this step is necessary so that the list of objects does not change in the temp step
            pks = list(objs.values_list('pk', flat=True))
            objs = cls.objects.filter(pk__in=pks)

            # first all of the indexes are set to their negative counterparts, to prevent unique constraint violations
            objs.update(index=F('index') * -1)
            # then they are set to the correct value
            if old_index < index:
                objs.update(index=F('index') * -1 - 1)
            elif old_index > index:
                objs.update(index=F('index') * -1 + 1)

            # finally, the original obj's index is reset from 0
            obj.index = index
            obj.save()

    except IntegrityError:
        index = 1
        for obj in cls.objects.filter(**initial_filters):
            obj.index = index
            obj.save()
            index += 1

    return MutationResult(ok=True)


def authenticated(func):
    def wrapper(self, info, *args, **kwargs):
        if not info.context.user.is_authenticated:
            permission_denied()
        return func(self, info, *args, **kwargs)

    return wrapper


def permission_denied():
    raise Exception('Permission denied')


def verify_permission(info, verify, obj):
    if not verify(info.context.user, obj):
        permission_denied()


def generate_unique_name(model, name='untitled', **filters):
    unique_name = name
    num = 0
    while model.objects.filter(name=unique_name, **filters).exists():
        unique_name = f'{name} {num}'
        num += 1
    return unique_name


def create_error(**kwargs):
    return MutationResult(ok=False, errors=[ModelError(**kwargs)])
