import graphene
from django.core.exceptions import ValidationError


def create_errors(error_dict):
    return [
        ModelError(field=key, message=value[0])
        for key, value in error_dict.items()
    ]


def validate(cls, model):
    try:
        model.full_clean()
    except ValidationError as e:
        return cls(ok=False, errors=create_errors(e.message_dict))
    model.save()
    return cls(ok=True)


def update(model, fields):
    for key, value in fields.items():
        setattr(model, key, value)


def authenticated(func):
    def wrapper(self, info, *args, **kwargs):
        if not info.context.user.is_authenticated:
            permission_denied()
        return func(self, info, *args, **kwargs)

    return wrapper


def permission_denied():
    raise Exception('Permission denied')


class ModelError(graphene.ObjectType):
    field = graphene.String(required=True)
    message = graphene.String(required=True)


class ModelMutation:
    ok = graphene.Boolean(required=True)
    errors = graphene.List(ModelError)
