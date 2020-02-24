import pytest

from src.plan.services import validate_indexes

PARENT_CLASSNAME = 'Parent'
CHILD_CLASSNAME = 'Child'


def test_validate_unsorted_lists():
    # The test passes if no exception is raised
    validate_indexes([1, 2, 0, 3], PARENT_CLASSNAME, CHILD_CLASSNAME)


def test_validate_first_index_is_zero():
    with pytest.raises(Exception) as exception:
        validate_indexes([1, 2, 3, 4], PARENT_CLASSNAME, CHILD_CLASSNAME)
    assert (
        exception._excinfo[1].args[0]
        == 'Missing first Parent, first Parent index must be 0 (zero).'
    )


def test_validate_indexes_do_not_have_gaps():
    with pytest.raises(Exception) as exception:
        validate_indexes([0, 1, 4, 5], PARENT_CLASSNAME, CHILD_CLASSNAME)
    assert (
        exception._excinfo[1].args[0]
        == 'Child with index 4 found after index 1, but index 2 was expected.'
    )


def test_validate_indexes_are_not_duplicated():
    with pytest.raises(Exception) as exception:
        validate_indexes(
            [0, 1, 2, 2, 3, 4, 4], PARENT_CLASSNAME, CHILD_CLASSNAME
        )
    assert (
        exception._excinfo[1].args[0]
        == 'Duplicated Child found in Parent: Child index 2 was found 2 times, Child index 4 was found 2 times'
    )
