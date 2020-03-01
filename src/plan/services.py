import datetime
from typing import Any, List, NoReturn, Optional, Union

import django
from django.db import transaction

from src.plan.models import (
    Exercise,
    ExerciseType,
    Goal,
    Loop,
    Plan,
    Record,
    Session,
)

NO_RECORDS: List[Record] = []
NO_LOOPS: List[Loop] = []


def get_default_from_model(
    model: django.db.models.Model, field_name: str
) -> Union[NoReturn, Any]:
    """Return the default value of a model field.

    If the field does not have a default value, an exception will be raised to
    warn the developer.
    """
    model_fields = model._meta.fields

    if field_name not in [field.name for field in model_fields]:
        raise Exception(
            f"The field '{field_name}' does not exist in the {model.__name__} model"
        )

    for field in model_fields:
        if field.name == field_name:
            return field.default
    raise Exception(
        f"Dear developer, sorry but the field '{field_name}'  (in the model {model.__name__}) does not have a default value"
    )


def validate_indexes(
    indexes: List[int], parent_classname: str, child_classname: str
) -> Optional[NoReturn]:
    """Check that the Parent in the Child have the right indexes."""
    indexes.sort()

    # First index must be zero
    if indexes[0] != 0:
        raise Exception(
            f'Missing first {parent_classname}, first {parent_classname} index must be 0 (zero).'
        )

    # No duplicated indexes allowed
    deduped_indexes = set(indexes)
    if len(deduped_indexes) != len(indexes):
        duplicated_indexes = []
        for index in indexes:
            if indexes.count(index) > 1:
                duplicated_indexes.append(index)
        msg = f'Duplicated {child_classname} found in {parent_classname}: '
        dupe_report = []
        for index in set(duplicated_indexes):
            ocurrences = duplicated_indexes.count(index)
            dupe_report.append(
                f'{child_classname} index {index} was found {ocurrences} times'
            )
        msg += (', ').join(dupe_report)
        raise Exception(msg)

    # Indexes must be sequential and have no gaps
    for index, reference in zip(indexes, range(len(indexes))):
        if index != reference:
            raise Exception(
                f'{child_classname} with index {index} found after index {reference - 1}, but index {reference} was expected.'
            )
    return None


def validate_goal_indexes(goals: List[Goal]) -> Optional[NoReturn]:
    """Check that the Goals in the Loop have the right indexes."""
    goal_indexes = [goal.goal_index for goal in goals]
    validate_indexes(goal_indexes, Loop.__name__, Goal.__name__)
    return None


def validate_loop_indexes(loops: List[Loop]) -> Optional[NoReturn]:
    """Check that the Loops in the Plan have the right indexes."""
    loop_indexes = [loop.loop_index for loop in loops]
    validate_indexes(loop_indexes, Plan.__name__, Loop.__name__)
    return None


def validate_loop_and_goal_indexes(loops: List[Loop]) -> Optional[NoReturn]:
    """Check that the Loops and Goals in the Plan have the right indexes.

    A loop_index represents the position of a Loop inside a Plan.
    A goal_index represents the position of a Goal inside a Loop.

    Both loops_index and goal_index must start on 0 (zero) and grow one by one
    withou skipping any number:

      - Good: 0, 1, 2, 3, 4
      - Bad:  1, 2, 3, 4, 5  --> Notice the first item is not 0
      - Bad:  0, 1, 7, 8, 9  --> Notice the gap between 1 and 7

    If the validation fails, an exception will be raise with the appropiate
    information. Otherwise, this function return None.
    """
    validate_loop_indexes(loops)
    for loop in loops:
        validate_goal_indexes(loop.goals)
    return None


class ExerciseService:
    @staticmethod
    def create(
        *,
        name: str,
        description: str = get_default_from_model(Exercise, 'description'),
        exercise_type: str,
    ) -> Exercise:
        exercise = Exercise(
            name=name, description=description, exercise_type=exercise_type
        )
        exercise.full_clean()
        exercise.save()
        return exercise

    @staticmethod
    def get_by_id(id: int) -> Optional[Exercise]:
        try:
            return Exercise.objects.get(pk=id)
        except Exercise.DoesNotExist:
            return None

    @staticmethod
    def get_or_create(
        *, name: str, description: str = None, exercise_type: str,
    ) -> Exercise:
        exercise = ExerciseService.get_if_exists(
            name=name, description=description, exercise_type=exercise_type,
        )
        if not exercise:
            if not description:
                description = get_default_from_model(Exercise, 'description')
            exercise = ExerciseService.create(
                name=name,
                description=description,
                exercise_type=exercise_type,
            )
        return exercise

    @staticmethod
    def get_if_exists(
        *, name: str, description: str = None, exercise_type: str,
    ) -> Optional[Exercise]:
        try:
            if description is None:
                return Exercise.objects.get(
                    name=name, exercise_type=exercise_type
                )
            return Exercise.objects.get(
                name=name,
                description=description,
                exercise_type=exercise_type,
            )
        except Exercise.DoesNotExist:
            return None

    @staticmethod
    def delete(*, id: int) -> bool:
        exercise = ExerciseService.get_by_id(id)
        if not exercise:
            return False
        deleted_resources = exercise.delete()
        # deleted_resources example:
        # (8, {'plan.Goal': 4, 'plan.Record': 3, 'plan.Exercise': 1})
        if len(deleted_resources) == 2:
            return True
        return False


class GoalService:
    @staticmethod
    def create(
        loop: Loop,
        exercise: Exercise,
        goal_index: int,
        duration: int,
        repetitions: int,
        pause: bool,
    ) -> Goal:
        goal = Goal(
            loop=loop,
            exercise=exercise,
            goal_index=goal_index,
            duration=duration,
            repetitions=repetitions,
            pause=pause,
        )
        goal.full_clean()
        goal.save()
        return goal


class LoopService:
    @staticmethod
    def create(
        *,
        plan: Plan,
        rounds: int = get_default_from_model(Loop, 'rounds'),
        loop_index: int,
        description: str = get_default_from_model(Loop, 'description'),
    ) -> Loop:
        loop = Loop(
            plan=plan,
            rounds=rounds,
            loop_index=loop_index,
            description=description,
        )
        loop.full_clean()
        loop.save()
        return loop


class PlanService:
    @staticmethod
    def create(
        *,
        name: str,
        description: str = None,
        created: datetime.datetime,
        loops: List[Loop] = NO_LOOPS,
    ) -> Plan:
        validate_loop_and_goal_indexes(loops)
        with transaction.atomic():
            plan = Plan(
                name=name,
                description=description,
                created=created,
                last_updated=created,
            )
            plan.full_clean()
            plan.save()

            for loop_data in loops:
                loop = Loop(
                    plan=plan,
                    rounds=loop_data.rounds,
                    loop_index=loop_data.loop_index,
                    description=loop_data.description,
                )
                loop.full_clean()
                loop.save()

                for goal_data in loop_data.goals:
                    exercise = ExerciseService.get_by_id(goal_data.exercise_id)
                    if not exercise:
                        raise Exception(
                            f'It was not possible to create Goal because there is no Exercise with ID {goal_data.exercise_id}. Loop {loop_data.loop_index}, Goal {goal_data.goal_index}'
                        )
                    goal = Goal(
                        loop=loop,
                        exercise=exercise,
                        goal_index=goal_data.goal_index,
                        duration=goal_data.duration,
                        repetitions=goal_data.repetitions,
                        pause=goal_data.pause,
                    )
                    goal.full_clean()
                    goal.save()

        return plan

    @staticmethod
    def get(*, name: str, created: datetime.datetime) -> Optional[Plan]:
        try:
            return Plan.objects.get(name=name, created=created)
        except Plan.DoesNotExist:
            return None


class RecordService:
    _reps_key = 'reps'
    _exercise_key = 'exercise'
    _reps_default_value = 0

    @classmethod
    def create(cls, **kwargs) -> Record:
        cls._validate_exercise_type_and_record_reps(**kwargs)
        record = Record(**kwargs)
        record.full_clean()
        return record.save()

    @classmethod
    def _validate_exercise_type_and_record_reps(
        cls, **kwargs
    ) -> Optional[NoReturn]:
        exercise_type = kwargs[cls._exercise_key].exercise_type
        reps = kwargs.get(cls._reps_key, cls._reps_default_value)

        if exercise_type == ExerciseType.REST and reps == 0:
            return None
        if exercise_type == ExerciseType.PREPARATION and reps == 0:
            return None
        # Exercises without reps are modelled as a big single rep
        if exercise_type == ExerciseType.WORK and reps > 0:
            return None
        msg = 'Ensure the exercise type and the record reps are aligned:\n'
        msg += f'  - if WORK type exercise --> record reps > 0'
        msg += f'  - if REST type exercise --> record reps = 0'
        msg += f'  - if PREP type exercise --> record reps = 0'
        msg += (
            f'Current case: {exercise_type} exercise type, {reps} record reps'
        )
        raise Exception(msg)


class SessionService:
    @classmethod
    def create(
        cls,
        *,
        name: str,
        description: str = get_default_from_model(Session, 'description'),
        notes: str = get_default_from_model(Session, 'notes'),
        start: datetime.datetime,
        records: List[Record] = NO_RECORDS,
    ) -> Session:
        with transaction.atomic():
            session = Session(
                name=name, description=description, notes=notes, start=start
            )
            session.full_clean()
            session.save()
            for record in records:
                exercise = ExerciseService.get_by_id(record.exercise_id)
                if not exercise:
                    raise Exception(
                        f"""Failed to create Record because there the Exercise with ID {record.exercise_id} does not exist. Record data: start={record.start.isoformat()}, end={record.end.isoformat()}"""
                    )
                RecordService.create(
                    start=record.start,
                    end=record.end,
                    reps=record.reps,
                    exercise=exercise,
                    session=session,
                )
            return session
