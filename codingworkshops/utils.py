# Creates a class to represent the errors returned by django model validation
# These errors exist for each property and are represented by a graphql list of strings
def create_error_class(model, properties):
    return type(
        f'Create{model}Errors', (graphene.ObjectType, ), {
            property: graphene.List(graphene.NonNull(graphene.String))
            for property in properties
        }
    )
