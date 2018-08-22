import graphene
from graphene_django.forms.mutation import DjangoModelFormMutation

from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django import forms

from .models import User


class LoginUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean(required=True)

    def mutate(self, info, username, password):
        # info.context is the django request
        user = authenticate(info.context, username=username, password=password)
        if user is not None:
            login(info.context, user)
            return LoginUser(ok=True)
        return LoginUser(ok=False)


class LogoutUser(graphene.Mutation):
    ok = graphene.Boolean(required=True)

    def mutate(self, info):
        logout(info.context)
        return LoginUser(ok=True)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'bio', 'location']


class CreateUser(DjangoModelFormMutation):
    class Meta:
        form_class = UserForm


class Mutation(graphene.ObjectType):
    login_user = LoginUser.Field()
    logout_user = LogoutUser.Field()
    create_user = CreateUser.Field()
