import datetime

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from src.plan.models import (
    Exercise,
    ExerciseType,
    Session,
    is_not_future_datetime,
)

EXERCISE_NAME = 'exercise test name'
SESSION_NAME = 'session test name'


@pytest.fixture
def now() -> datetime.datetime:
    return timezone.now()


@pytest.fixture
def past_datetime(now) -> datetime.datetime:
    print(now - datetime.timedelta(hours=2))
    return now - datetime.timedelta(hours=2)


@pytest.fixture
def future_datetime(now) -> datetime.datetime:
    print(now + datetime.timedelta(hours=2))
    return now + datetime.timedelta(hours=2)


@pytest.fixture
def exercise(past_datetime: datetime.datetime) -> Exercise:
    exercise = Exercise(name=EXERCISE_NAME, type=ExerciseType.WORK)
    exercise.save()
    return exercise


@pytest.fixture
def session(past_datetime: datetime.datetime) -> Session:
    session = Session(name=SESSION_NAME, start=past_datetime)
    session.save()
    return session


def test_does_not_raise_exception_if_is_past_datetime(past_datetime):
    is_not_future_datetime(past_datetime)


def test_raises_exception_if_is_future_datetime(future_datetime):
    with pytest.raises(ValidationError):
        is_not_future_datetime(future_datetime)


def test_session_cannot_start_in_the_future(future_datetime):
    with pytest.raises(ValidationError):
        session = Session(name=SESSION_NAME, start=future_datetime)
        session.full_clean()  # trigger validations


@pytest.mark.skip
@pytest.mark.django_db
@pytest.mark.parametrize('start,end', ((past_datetime, future_datetime),))
def test_record_must_start_and_end_in_the_past(session, exercise, start, end):
    pass
    # with pytest.raises(ValidationError):
    #     record = Record(
    #         session=session, exercise=exercise, start=start, end=end
    #     )
    #     import ipdb

    #     ipdb.set_trace()
    #     record.full_clean()  # trigger validations
