import graphene
from graphene_django.types import DjangoObjectType

from django.contrib.auth import authenticate, login, logout

from .models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude_fields = ['password']


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, username=graphene.String(required=True))
    me = graphene.Field(UserType)

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self, info, **kwargs):
        return User.objects.get(username=kwargs.get('username'))

    def resolve_me(self, info, **kwargs):
        if info.context.user.is_authenticated:
            return info.context.user
        else:
            return None


class LoginUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, username, password):
        # info.context is the django request
        user = authenticate(username=username, password=password)
        if user is not None:
            login(info.context, user)
            return LoginUser(ok=True)
        else:
            return LoginUser(ok=False)


class LogoutUser(graphene.Mutation):
    ok = graphene.Boolean()

    def mutate(self, info):
        logout(info.context)
        return LoginUser(ok=True)


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        bio = graphene.String()
        birth_date = graphene.types.datetime.Date()
        location = graphene.String()

    Output = UserType

    def mutate(self, info, username, password, email, **kwargs):
        return User.objects.create_user(
            username=username,
            password=password,
            email=email,
            # because these are optional
            bio=kwargs.get('bio'),
            birth_date=kwargs.get('birth_date'),
            location=kwargs.get('location')
        )


class Mutation(graphene.ObjectType):
    login_user = LoginUser.Field()
    logout_user = LogoutUser.Field()
    create_user = CreateUser.Field()
