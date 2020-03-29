import pytest
from graphene.test import Client

from tests.plan.conftest import ExerciseFactory

ERRORS = 'errors'

GET_EXERCISES = '''
{
    exercises {
        id
        name
        description
        exerciseType
    }
}
'''


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_get_exercises(
    graphql_client: Client, create_exercises: ExerciseFactory
) -> None:
    """
    Given I am a developer
    And there are 2 exercises
    When I ask to see all the exercises
    Then I get all the exercises
    """
    create_exercises(amount=2)

    response = graphql_client.execute(GET_EXERCISES)
    assert ERRORS not in response
    assert response['data'] == {
        'exercises': [
            {
                'id': '1',
                'name': 'sample exercise name 0',
                'description': 'sample exercise description 0',
                'exerciseType': 'WORK',
            },
            {
                'id': '2',
                'name': 'sample exercise name 1',
                'description': 'sample exercise description 1',
                'exerciseType': 'WORK',
            },
        ]
    }
