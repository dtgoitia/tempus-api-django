import graphene

import src.plan.api.graphql.queries


class Query(src.plan.api.graphql.queries.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
