import graphene

from graphene_django.types import DjangoObjectType

from .models import Workshop


class WorkshopType(DjangoObjectType):
    class Meta:
        model = Workshop


class Query(graphene.ObjectType):
    all_workshops = graphene.List(WorkshopType)
    workshop = graphene.Field(
        WorkshopType, name=graphene.String(required=True)
    )

    def resolve_all_workshops(self, info, **kwargs):
        return Workshop.objects.all()

    def resolve_workshop(self, info, **kwargs):
        return Workshop.objects.get(name=kwargs.get("name"))


class CreateWorkshop(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)

    Output = WorkshopType

    def mutate(self, info, name, description):
        return Workshop.objects.create(name=name, description=description)


class Mutation(graphene.ObjectType):
    create_workshop = CreateWorkshop.Field()
