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
