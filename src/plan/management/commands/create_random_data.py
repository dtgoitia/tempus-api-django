import time
import uuid

from django.core.management.base import BaseCommand
from django.utils import timezone

from src.plan.models import (
    Exercise,
    ExerciseType,
    Goal,
    Loop,
    Plan,
    Record,
    Session,
)


def create_uuid() -> str:
    return str(uuid.uuid4())


def generate_exercise() -> Exercise:
    exercise = Exercise(
        name=f"exercise name {create_uuid()}",
        description=f"exercise description {create_uuid()}",
        type=ExerciseType.WORK,
    )
    exercise.save()
    return exercise


def generate_goal(loop: Loop, index: int, exercise: Exercise) -> Goal:
    goal = Goal(
        loop=loop,
        exercise=exercise,
        goal_index=index,
        duration=10,
        repetitions=3,
        description=f"description of the Goal {create_uuid()}",
    )
    goal.save()
    return goal


def generate_loop(plan: Plan, index: int) -> Loop:
    loop = Loop(
        plan=plan,
        rounds=2,
        loop_index=index,
        description=f"description of the Loop {create_uuid()}",
    )
    loop.save()
    return loop


def generate_plan() -> Plan:
    plan = Plan(
        name=f"plan name {create_uuid()}",
        description=f"plan description {create_uuid()}",
    )
    plan.save()
    return plan


def generate_session() -> Session:
    session = Session(name='my session', start=timezone.now())
    session.save()
    return session


def generate_record(session: Session, exercise: Exercise) -> Record:
    start = timezone.now()
    time.sleep(0.01)
    end = timezone.now()
    record = Record(session=session, exercise=exercise, start=start, end=end)
    record.save()
    return record


def generate_whole_session() -> None:
    session = generate_session()
    exercise = Exercise.objects.first()
    generate_record(session, exercise)
    generate_record(session, exercise)
    generate_record(session, exercise)


class Command(BaseCommand):
    help = "Creates random plan data"

    def handle(self, *args, **kwargs):
        plan = generate_plan()

        loops = [generate_loop(plan, i) for i in range(4)]

        exercises = [(generate_exercise(), i) for i in range(3)]

        goals = []
        for loop in loops:
            for exercise, i in exercises:
                goal = generate_goal(loop, i, exercise)
                goals.append(goal)

        generate_whole_session()
