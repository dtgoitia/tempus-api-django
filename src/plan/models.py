import datetime
from typing import NoReturn, Optional

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

EMPTY_STRING = ''


def is_not_future_datetime(value: datetime.datetime) -> Optional[NoReturn]:
    now = timezone.now()
    if now < value:
        raise ValidationError(
            f'The value {value.isoformat()} must not be in the future'
        )
    return None


def is_positive_number(value: int) -> Optional[NoReturn]:
    if value <= 0:
        raise ValidationError(f'The value {value} must be positive')
    return None


class ExerciseType(models.TextChoices):
    WORK = 'WORK'
    REST = 'REST'
    PREPARATION = 'PREP'


class Exercise(models.Model):
    name = models.TextField(
        null=False,
        help_text='Short name for the user to identify the exercise.',
    )
    description = models.TextField(
        default=EMPTY_STRING,
        help_text='Optional space for details about the exercise, technique, caveats...',
    )
    # TODO: use DjangoChoicesEnum, from django_graphene
    exercise_type = models.CharField(
        max_length=4, choices=ExerciseType.choices, null=False
    )

    def __repr__(self) -> str:
        return f"<Exercise '{self.name}' #{self.id}>"


class Goal(models.Model):
    loop = models.ForeignKey(
        "Loop", on_delete=models.CASCADE, related_name="goals",
    )
    exercise = models.ForeignKey(
        Exercise, related_name="+", on_delete=models.CASCADE
    )
    goal_index = models.IntegerField(
        null=False,
        validators=[is_positive_number],
        help_text='Position of the Goal inside the parent Loop.',
    )
    duration = models.IntegerField(
        null=True,
        validators=[is_positive_number],
        help_text='Time allocated to execute the Exercise.',
    )
    repetitions = models.IntegerField(
        null=True,
        validators=[is_positive_number],
        help_text='Amount of times the Exercise should be repeated during a single execution of the Goal.',
    )
    pause = models.BooleanField(
        null=False,
        default=False,
        help_text='Specifies if the goal waits for users approval to run or not.',
    )

    def __repr__(self) -> str:
        return f"<Goal #{self.id}>"


class Loop(models.Model):
    plan = models.ForeignKey(
        "Plan", on_delete=models.CASCADE, related_name="loops",
    )
    rounds = models.IntegerField(
        null=False,
        default=1,
        validators=[is_positive_number],
        help_text='Amount of times that the whole block of child Goals under the Loop will be executed.',
    )
    loop_index = models.IntegerField(
        null=False,
        validators=[is_positive_number],
        help_text='Position of the Loop inside the parent Plan.',
    )
    description = models.TextField(
        default=EMPTY_STRING,
        help_text='Optional description for a group of goals.',
    )

    def __repr__(self) -> str:
        return f"<Loop #{self.id}>"


class Plan(models.Model):
    name = models.TextField(
        null=False, help_text='Short name for the user to identify the plan.',
    )
    description = models.TextField(
        default=EMPTY_STRING,
        help_text='Optional space for a longer description of what the plan is about.',
    )
    created = models.DateTimeField(
        null=False,
        help_text='Moment at which the plan was created in the client. This time has nothing to do with when was the plan saved in the backend.',
    )
    last_updated = models.DateTimeField(
        null=False,
        help_text='Moment at which the plan was update for last time in the client. This time has nothing to do with when was the plan updated in the backend.',
    )

    def __repr__(self) -> str:
        return f"<Plan '{self.name}'>"


class Session(models.Model):
    name = models.TextField(
        null=False,
        help_text='Short name for the user to identify the session.',
    )
    description = models.TextField(
        default=EMPTY_STRING,
        help_text='Short description for the user to get a better understanding of what the session is about.',
    )
    notes = models.TextField(
        default=EMPTY_STRING,
        help_text='Optional space for notes like: what went well/bad, injuries, why the session was aborted...',
    )

    # The start time of the session and the start time of the first record
    # might differ, e.g.: the user starts a session, goes to prepare material,
    # and then starts executing exercises - there is a time gap between the
    # session start and the first executed exercise start.
    # auto_now=False because the time will be recorded by the client, which
    # could be communicated hours later to the server
    start = models.DateTimeField(
        auto_now=False,
        null=False,
        help_text='Moment at which the session started.',
        validators=[is_not_future_datetime],
    )

    def __repr__(self) -> str:
        return f"<Session '{self.name}'>"


class Record(models.Model):
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name='records', null=False,
    )
    exercise = models.ForeignKey(
        Exercise, on_delete=models.CASCADE, related_name='+', null=False
    )

    # auto_now=False because the time will be recorded by the client, which
    # could be communicated hours later to the server
    start = models.DateTimeField(
        auto_now=False,
        null=False,
        help_text='Moment at which the execution of the exercise started.',
        validators=[is_not_future_datetime],
    )
    # auto_now=False because the time will be recorded by the client, which
    # could be communicated hours later to the server
    end = models.DateTimeField(
        auto_now=False,
        null=False,
        help_text='Moment at which the execution of the exercise finished.',
        validators=[is_not_future_datetime],
    )

    reps = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text='Amount of times the execise was repeated during the record.',
    )

    def __repr__(self) -> str:
        return f"<Record '{self.exercise.name}'>"
