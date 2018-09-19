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


