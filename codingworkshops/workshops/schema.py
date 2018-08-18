import graphene

from graphene_django.types import DjangoObjectType

from .models import Workshop


class WorkshopType(DjangoObjectType):
    class Meta:
        model = Workshop


class Query(object):
    all_workshops = graphene.List(WorkshopType)
    workshop = graphene.Field(WorkshopType, name=graphene.String())

    def resolve_all_workshops(self, info, **kwargs):
        return Workshop.objects.all()

    def resolve_workshop(self, info, **kwargs):
        return Workshop.objects.get(name=kwargs.get('name'))

