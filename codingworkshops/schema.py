import graphene

import codingworkshops.workshops.schema


class Query(codingworkshops.workshops.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

schema = graphene.Schema(query=Query)
