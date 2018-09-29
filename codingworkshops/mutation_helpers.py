from django.core.exceptions import ValidationError
from django.db.models import F
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


def move(cls, obj, index):
    # change the id to avoid uniqueness violation error
    old_index = obj.index
    obj.index = -1
    obj.save()
    # change other object ids
    if old_index < index:
        cls.objects.filter(
            index__gt=old_index, index__lte=index
        ).update(index=F('index') - 1)
    elif old_index > index:
        cls.objects.filter(
            index__gte=index, index__lt=old_index
        ).update(index=F('index') + 1)
    # set the id to the new id
    obj.index = index
    obj.save()
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
