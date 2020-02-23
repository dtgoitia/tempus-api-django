import datetime
from typing import Any, NoReturn, Optional, Union

import django

from src.plan.models import (
    Exercise,
    ExerciseType,
    Goal,
    Loop,
    Plan,
    Record,
    Session,
)


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


class ExerciseService:
    @staticmethod
    def create(
        *,
        name: str,
        description: str = get_default_from_model(Exercise, 'description'),
        exercise_type: str,
    ) -> Exercise:
        exercise = Exercise(
            name=name, description=description, type=exercise_type
        )
        exercise.full_clean()
        exercise.save()
        return exercise

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
        *, name: str, description: str = None, created: datetime.datetime
    ) -> Plan:
        if description is None:
            plan = Plan(name=name, created=created, last_updated=created)
        else:
            plan = Plan(
                name=name,
                description=description,
                created=created,
                last_updated=created,
            )
        plan.full_clean()
        plan.save()
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
        exercise_type = kwargs[cls._exercise_key].type
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
    @staticmethod
    def create(
        *,
        name: str,
        description: str = get_default_from_model(Session, 'description'),
        notes: str = get_default_from_model(Session, 'notes'),
        start: datetime.datetime,
    ) -> Session:
        session = Session(
            name=name, description=description, notes=notes, start=start
        )
        session.full_clean()
        return session.save()
