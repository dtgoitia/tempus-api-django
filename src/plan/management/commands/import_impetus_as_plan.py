"""IMPORTANT
This command imports Impetus XML files as if they were Plans. However, those
XML files are not Plans, but Records.

Use this command only to import Impetus XML files which contain Plans.
"""
import datetime
import os
from typing import Dict, Tuple
from xml.etree import ElementTree

import pytz
from django.core.management.base import BaseCommand

from src.plan.management.utils import get_exercise_type, parse_xml
from src.plan.models import Loop, Plan
from src.plan.services import (
    ExerciseService,
    GoalService,
    LoopService,
    PlanService,
)

FILES_OPTION = 'files'
TIME_ATTRIB = 'time'
ROUNDS_ATTRIB = 'rounds'
PAUSE_ATTRIB = 'pause'
DEFAULT_REPS = 1


class Command(BaseCommand):
    help = "Import the XML data exported by Impetus"

    def add_arguments(self, parser):
        parser.add_argument(FILES_OPTION, nargs='+', type=str)

    def handle(self, *args, **options) -> None:
        files = options.get(FILES_OPTION)
        if not files:
            return None
        # TODO: add logging everywhere

        for path in files:
            abs_path = os.path.abspath(path)
            import_impetus_file(abs_path)


def import_impetus_file(path: str) -> None:
    with open(path, 'r') as f:
        content = f.read()
        tree = parse_xml(content)
        for plan_xml in tree:
            # TODO: validate here or where?
            parse_plan(plan_xml)


def parse_plan(plan_xml: ElementTree.Element) -> None:
    TIMER_TAG = 'btimer'
    LOOP_TAG = 'loop'

    name = plan_xml.attrib['desc']
    created = datetime.datetime.strptime(
        plan_xml.attrib['desc'], '%Y-%m-%d'
    ).replace(tzinfo=pytz.utc)
    plan = PlanService.get(name=name, created=created)
    if not plan:
        description = plan_xml.attrib['summary']
        plan = PlanService.create(
            name=name, description=description, created=created,
        )

    for i, child in enumerate(plan_xml.getchildren()):
        if child.tag == TIMER_TAG:
            import_top_level_btimer(plan, child, i)
        if child.tag == LOOP_TAG:
            import_loop(plan, child, i)


def import_btimer(loop: Loop, btimer_xml: ElementTree.Element, index: int):
    exercise = ExerciseService.get_or_create(
        name=btimer_xml.attrib['desc'],
        exercise_type=get_exercise_type(btimer_xml),
    )
    duration, reps = get_duration_and_reps(btimer_xml.attrib)
    GoalService.create(
        loop=loop,
        exercise=exercise,
        goal_index=index,
        duration=duration,
        repetitions=reps,
        pause=True if btimer_xml.attrib[PAUSE_ATTRIB] == '0' else False,
    )


def import_top_level_btimer(
    plan: Plan, btimer_xml: ElementTree.Element, index: int
):
    loop = LoopService.create(plan=plan, rounds=1, loop_index=index)
    import_btimer(loop, btimer_xml, 1)


def import_loop(plan: Plan, loop_xml: ElementTree.Element, index: int):
    loop = LoopService.create(
        plan=plan, rounds=int(loop_xml.attrib[ROUNDS_ATTRIB]), loop_index=index
    )
    for i, child in enumerate(loop_xml.getchildren()):
        import_btimer(loop, child, i)


def get_duration_and_reps(child_attributes: Dict[str, str]) -> Tuple[int, int]:
    duration = child_attributes[TIME_ATTRIB]
    return (int(duration), DEFAULT_REPS)
