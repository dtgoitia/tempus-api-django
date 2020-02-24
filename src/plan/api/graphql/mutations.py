import datetime
from typing import List

import graphene

from src.plan.api.graphql import types
from src.plan.models import Record
from src.plan.services import ExerciseService, SessionService

NO_RECORDS: List[Record] = []


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
    create_session = CreateSession.Field()
