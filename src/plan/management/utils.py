from xml.etree import ElementTree

from src.plan.services import ExerciseType

WORK_ATTRIB = 'work'
DESCRIPTION_ATTRIB = 'desc'
PAUSE_ATTRIB = 'pause'
PREPARATION_DESCRIPTIONS = ('Start', 'Now ', 'Get ready')


def get_exercise_type(exercise_xml: ElementTree.Element) -> str:
    is_work = bool(int(exercise_xml.attrib[WORK_ATTRIB]))
    if is_work:
        return ExerciseType.WORK
    if is_preparation(exercise_xml):
        return ExerciseType.REST
    return ExerciseType.REST


def is_preparation(exercise_xml: ElementTree.Element) -> bool:
    pause_enabled = bool(int(exercise_xml.attrib[PAUSE_ATTRIB]))
    if not pause_enabled:
        return False

    description = exercise_xml.attrib[DESCRIPTION_ATTRIB]
    for text_chunk in PREPARATION_DESCRIPTIONS:
        if text_chunk in description:
            return True
    raise Exception('Something unexpeceted happened here, checek exercise_xml')


def parse_xml(content: str) -> ElementTree.Element:
    # TODO: handle edge cases like is not an XML, etc
    result = ElementTree.fromstring(content)
    return result
