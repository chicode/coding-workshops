import graphene

import codingworkshops.workshops.schema
import codingworkshops.users.schema


class Query(codingworkshops.workshops.schema.Query,
            codingworkshops.users.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(codingworkshops.workshops.schema.Mutation,
               codingworkshops.users.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
