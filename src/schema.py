import graphene

import src.plan.api.graphql.mutations
import src.plan.api.graphql.queries


class Query(src.plan.api.graphql.queries.Query, graphene.ObjectType):
    pass


class Mutation(src.plan.api.graphql.mutations.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
