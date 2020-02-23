import graphene
from graphene_django.types import DjangoObjectType

from src.plan.models import Exercise, Goal, Loop, Plan, Record, Session


class ExerciseGraphqlType(DjangoObjectType):
    class Meta:
        model = Exercise


class GoalGraphqlType(DjangoObjectType):
    class Meta:
        model = Goal


class LoopGraphqlType(DjangoObjectType):
    class Meta:
        model = Loop


class PlanGraphqlType(DjangoObjectType):
    class Meta:
        model = Plan


class RecordGraphqlType(DjangoObjectType):
    class Meta:
        model = Record


class SessionGraphqlType(DjangoObjectType):
    class Meta:
        model = Session


class Query(object):
    plans = graphene.List(PlanGraphqlType)
    sessions = graphene.List(SessionGraphqlType)
    exercise = graphene.Field(
        ExerciseGraphqlType, exercise_id=graphene.String()
    )
    exercises = graphene.List(ExerciseGraphqlType)

    def resolve_plans(self, info, **kwargs):
        return Plan.objects.all()

    def resolve_sessions(self, info, **kwargs):
        return Session.objects.all()

    def resolve_exercise(self, info, exercise_id):
        return Exercise.objects.get(pk=exercise_id)

    def resolve_exercises(self, info, **kwargs):
        return Exercise.objects.all()
