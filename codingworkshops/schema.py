import graphene

import codingworkshops.workshops.query
import codingworkshops.workshops.mutation
import codingworkshops.users.query
import codingworkshops.users.mutation


class Query(
    codingworkshops.workshops.query.Query, codingworkshops.users.query.Query,
    graphene.ObjectType
):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(
    codingworkshops.workshops.mutation.Mutation,
    codingworkshops.users.mutation.Mutation, graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
