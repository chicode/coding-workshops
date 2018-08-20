import graphene
import graphene_django.types

from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout

from .models import User


class UserType(graphene_django.types.DjangoObjectType):
    class Meta:
        model = User
        exclude_fields = ['password']


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, username=graphene.String(required=True))
    current_user = graphene.Field(UserType)

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self, info, **kwargs):
        return User.objects.get(username=kwargs.get('username'))

    def resolve_current_user(self, info, **kwargs):
        if info.context.user.is_authenticated:
            return info.context.user
        return None


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


class CreateUserErrors(graphene.ObjectType):
    username = graphene.String()
    password = graphene.String()
    email = graphene.String()
    bio = graphene.String()
    birth_date = graphene.String()
    location = graphene.String()


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        bio = graphene.String()
        birth_date = graphene.types.datetime.Date()
        location = graphene.String()

    ok = graphene.Boolean(required=True)
    errors = graphene.Field(CreateUserErrors)

    def mutate(self, info, username, password, email, **kwargs):
        user = User(
            username=username,
            password=password,
            email=email,
            # because these are optional
            bio=kwargs.get('bio'),
            birth_date=kwargs.get('birth_date'),
            location=kwargs.get('location')
        )

        try:
            user.full_clean()
        except ValidationError as e:
            return CreateUser(
                ok=False, errors=CreateUserErrors(**e.message_dict)
            )

        user.save()
        return CreateUser(ok=True)


class Mutation(graphene.ObjectType):
    login_user = LoginUser.Field()
    logout_user = LogoutUser.Field()
    create_user = CreateUser.Field()
