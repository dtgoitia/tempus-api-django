from typing import Callable, List

import pytest
from mypy_extensions import NamedArg

from src.plan.models import Exercise, ExerciseType
from src.plan.services import ExerciseService

ExerciseFactory = Callable[[NamedArg(int, 'amount')], List[Exercise]]


@pytest.fixture
def create_exercises() -> ExerciseFactory:
    def exercise_factory(*, amount: int) -> List[Exercise]:
        exercises = [
            ExerciseService.create(
                name=f'sample exercise name {i}',
                description=f'sample exercise description {i}',
                exercise_type=ExerciseType.WORK,
            )
            for i in range(amount)
        ]
        return exercises

    return exercise_factory
