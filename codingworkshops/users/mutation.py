import graphene
from django.contrib.auth import authenticate, login, logout

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
        user = User(**kwargs)
        return validate(CreateUser, user)


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
        return validate(EditUser, user)


# Top-level


class Mutation(graphene.ObjectType):
    login_user = LoginUser.Field()
    logout_user = LogoutUser.Field()

    create_user = CreateUser.Field()
    edit_user = EditUser.Field()
