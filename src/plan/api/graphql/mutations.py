import datetime
from typing import List

import graphene

from src.plan.api.graphql import types
from src.plan.models import Loop, Record
from src.plan.services import ExerciseService, PlanService, SessionService

NO_RECORDS: List[Record] = []
NO_LOOPS: List[Loop] = []


class GoalsInput(graphene.InputObjectType):
    goal_index = graphene.Int(required=True)
    exercise_id = graphene.Int(required=True)
    repetitions = graphene.Int(required=True)
    duration = graphene.Int(required=True)
    pause = graphene.Boolean(required=True)


class LoopInput(graphene.InputObjectType):
    rounds = graphene.Int(required=True)
    description = graphene.String(required=False)
    loop_index = graphene.Int(required=True)
    goals = graphene.List(GoalsInput, required=True)


class CreatePlan(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=False)
        created = graphene.DateTime(required=True)
        loops = graphene.List(LoopInput, required=True)

    plan = graphene.Field(types.PlanGraphqlType)

    @staticmethod
    def mutate(
        root,
        info,
        name: str,
        description: str,
        created: datetime.datetime,
        loops: List[Loop] = NO_LOOPS,
    ) -> 'CreatePlan':
        """Create a Plan and return it."""
        plan = PlanService.create(
            name=name, description=description, created=created, loops=loops
        )
        return CreatePlan(plan=plan)


class CreateExercise(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=False)
        exercise_type = graphene.Argument(
            types.ExerciseTypeGraphqlType, required=True
        )

    exercise = graphene.Field(types.ExerciseGraphqlType)

    @staticmethod
    def mutate(
        root, info, name: str, description: str, exercise_type: str
    ) -> 'CreateExercise':
        """Create an Exercise and return it."""
        exercise = ExerciseService.create(
            name=name, description=description, exercise_type=exercise_type
        )
        return CreateExercise(exercise=exercise)


class RecordInput(graphene.InputObjectType):
    exercise_id = graphene.String(required=True)
    start = graphene.DateTime(required=True)
    end = graphene.DateTime(required=True)
    reps = graphene.Int(required=True)


class CreateSession(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=False)
        notes = graphene.String(required=False)
        start = graphene.DateTime(required=True)
        records = graphene.List(RecordInput, required=False)

    session = graphene.Field(types.SessionGraphqlType)

    @staticmethod
    def mutate(
        root,
        info,
        name: str,
        start: datetime.datetime,
        description: str = None,
        notes: str = None,
        records: List[Record] = NO_RECORDS,
    ) -> 'CreateSession':
        """Create a Session and return it."""
        args = {'name': name, 'start': start, 'records': records}
        if description:
            args.update({'description': description})
        if notes:
            args.update({'notes': notes})

        session = SessionService.create(**args)  # type: ignore
        return CreateSession(session=session)


class Mutation:
    create_exercise = CreateExercise.Field()
    create_plan = CreatePlan.Field()
    create_session = CreateSession.Field()
