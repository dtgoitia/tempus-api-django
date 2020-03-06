import graphene

from src.plan.api.graphql import types
from src.plan.models import Exercise, Plan, Session


class Query(object):
    plans = graphene.List(types.PlanGraphqlType)
    plan = graphene.Field(types.PlanGraphqlType, plan_id=graphene.String())
    sessions = graphene.List(types.SessionGraphqlType)
    exercise = graphene.Field(
        types.ExerciseGraphqlType, exercise_id=graphene.String()
    )
    exercises = graphene.List(types.ExerciseGraphqlType)

    def resolve_plan(self, info, plan_id):
        return Plan.objects.get(pk=plan_id)

    def resolve_plans(self, info, **kwargs):
        return Plan.objects.all()

    def resolve_sessions(self, info, **kwargs):
        return Session.objects.all()

    def resolve_exercise(self, info, exercise_id):
        return Exercise.objects.get(pk=exercise_id)

    def resolve_exercises(self, info, **kwargs):
        return Exercise.objects.all()
