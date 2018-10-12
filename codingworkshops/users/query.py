import graphene
import graphene_django.types

from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout

from .models import User


class UserType(graphene_django.types.DjangoObjectType):
    class Meta:
        model = User
        only_fields = ['username', 'email', 'bio', 'location']


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, human=graphene.String(required=True))
    current_user = graphene.Field(UserType)

    def resolve_all_users(self, info):
        return User.objects.all()

    def resolve_user(self, info, human):
        return User.objects.get(username=human)

    def resolve_current_user(self, info):
        if info.context.user.is_authenticated:
            return info.context.user
        return None
