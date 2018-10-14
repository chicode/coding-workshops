import graphene
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

from .models import User
from ..mutation_helpers import *

# Authentication


class LoginUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean(required=True)

    def mutate(self, info, **kwargs):
        user = authenticate(info.context, **kwargs)
        if user is not None:
            login(info.context, user)
            return LoginUser(ok=True)
        return LoginUser(ok=False)


class LogoutUser(graphene.Mutation):
    ok = graphene.Boolean(required=True)

    def mutate(self, info):
        logout(info.context)
        return LoginUser(ok=True)


# User


class CreateUser(ModelMutation, graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

        bio = graphene.String()
        location = graphene.String()

    def mutate(self, info, **kwargs):
        password = kwargs.get('password')
        user = User(password=make_password(kwargs.pop('password')), **kwargs)
        try:
            validate_password(password, user=user)
        except ValidationError as e:
            return MutationResult(
                ok=False, errors=create_errors({
                    'password': e.messages
                })
            )
        return validate(user)


class EditUser(ModelMutation, graphene.Mutation):
    class Arguments:
        pk_username = graphene.String(required=True)

        email = graphene.String()
        bio = graphene.String()
        location = graphene.String()
        password = graphene.String()

    @authenticated
    def mutate(self, info, **kwargs):
        user = User.objects.get(username=kwargs.pop('pk_username'))
        if info.context.user.username != user.username:
            permission_denied()
        update(user, kwargs)
        return validate(user)


# Top-level


class Mutation(graphene.ObjectType):
    login_user = LoginUser.Field()
    logout_user = LogoutUser.Field()

    create_user = CreateUser.Field()
    edit_user = EditUser.Field()
