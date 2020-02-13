import uuid

from django.core.management.base import BaseCommand

from src.plan.models import Exercise, Goal, Loop, Plan


def create_uuid() -> str:
    return str(uuid.uuid4())


def generate_exercise() -> Exercise:
    exercise = Exercise(
        name=f"exercise name {create_uuid()}",
        description=f"exercise description {create_uuid()}",
    )
    exercise.save()
    return exercise


def generate_goal(loop: Loop, index: int, exercise: Exercise) -> Goal:
    goal = Goal(
        loop=loop,
        exercise=exercise,
        entry_index=index,
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
