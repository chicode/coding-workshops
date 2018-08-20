import graphene
import graphene_django.types

from django.core.exceptions import ValidationError

from .models import Workshop


class WorkshopType(graphene_django.types.DjangoObjectType):
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


class CreateWorkshopErrors(graphene.ObjectType):
    name = graphene.String()
    description = graphene.String()


class CreateWorkshop(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)

    ok = graphene.Boolean(required=True)
    errors = graphene.Field(CreateWorkshopErrors)

    def mutate(self, info, name, description):
        workshop = Workshop(name=name, description=description)

        try:
            workshop.full_clean()
        except ValidationError as e:
            return CreateWorkshop(
                ok=False, errors=CreateWorkshopErrors(**e.message_dict)
            )

        workshop.save()
        return CreateWorkshop(ok=True)


class Mutation(graphene.ObjectType):
    create_workshop = CreateWorkshop.Field()
