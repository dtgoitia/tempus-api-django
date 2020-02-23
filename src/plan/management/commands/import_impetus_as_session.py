"""IMPORTANT
This command imports Impetus XML files as if they were Sessions.

Use this command only to import Impetus XML files which contain Sessions.
"""
import datetime
import os
from xml.etree import ElementTree

from django.core.management.base import BaseCommand

from src.plan.management.utils import get_exercise_type, parse_xml
from src.plan.models import Exercise, ExerciseType, Session
from src.plan.services import ExerciseService, RecordService, SessionService

FILES_OPTION = 'files'
TIMER_TAG = 'btimer'
LOOP_TAG = 'loop'
DESCRIPTION_ATTRIB = 'desc'
SUMMARY_ATTRIB = 'summary'
TIME_ATTRIB = 'time'
ROUNDS_ATTRIB = 'rounds'


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
        for session_xml in tree:
            # TODO: validate here or where?
            parse_session(session_xml)


def parse_session(session_xml: ElementTree.Element) -> None:
    start = get_start(session_xml)
    session_attributes = {
        'name': session_xml.attrib[DESCRIPTION_ATTRIB],
        'description': session_xml.attrib[SUMMARY_ATTRIB],
        'start': start,
    }

    session = SessionService.create(**session_attributes)

    # The 'btimer' and 'loop' only contain duration, which is fine in the realm
    # of planning, but we are creating records here with real start and end
    # timestamps.
    # Also, in the realm of records, there is not such thing as a loop, only a
    # flat structure of records within a session. This means is necessary to
    # flatten the content within the loop (and multiply it as needed). To
    # create records one after another, a cursor will be used ('t'), which will
    # contain the 'end' datetime of the last added record (for a the current
    # session). The next record will start where the previous one finishes.
    t: datetime.datetime = start
    for i, child in enumerate(session_xml.getchildren()):
        if child.tag == TIMER_TAG:
            t = import_btimer(session, child, t)
        if child.tag == LOOP_TAG:
            t = import_loop(session, child, t)


def import_btimer(
    session: Session, btimer_xml: ElementTree.Element, start: datetime.datetime
) -> datetime.datetime:
    exercise = ExerciseService.get_or_create(
        name=btimer_xml.attrib['desc'],
        exercise_type=get_exercise_type(btimer_xml),
    )
    duration = int(btimer_xml.attrib[TIME_ATTRIB])
    reps = None
    if exercise.type == ExerciseType.WORK:
        reps = get_reps(exercise)
    end = start + datetime.timedelta(seconds=duration)
    RecordService.create(
        session=session, exercise=exercise, start=start, end=end, reps=reps
    )
    return end


def import_loop(
    session: Session,
    session_xml: ElementTree.Element,
    start: datetime.datetime,
) -> datetime.datetime:
    t = start
    round_amount = int(session_xml.attrib[ROUNDS_ATTRIB])
    for round in range(round_amount):
        for btimer_xml in session_xml.getchildren():
            t = import_btimer(session, btimer_xml, t)
    return t


def get_start(session_xml: ElementTree.Element) -> datetime.datetime:
    description = session_xml.attrib[DESCRIPTION_ATTRIB]

    try:
        start = datetime.datetime.strptime(description, '%Y-%m-%d')
    except TypeError:
        raise Exception(
            f'Not possible to understand the Session start datetime from its description: {description}'
        )
    return start


def get_reps(exercise: Exercise) -> int:
    # TODO: find a way of mapping the exercise description to the amount of reps
    EXERCISE_REPS_MAP = {'': 1}
    return EXERCISE_REPS_MAP[exercise.name]
