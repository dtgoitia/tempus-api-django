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

CREATE_EXERCISE = '''
mutation createExercise(
  $name: String!,
  $description: String,
  $exerciseType: ExerciseType!
) {
  createExercise (
    name: $name,
    description: $description,
    exerciseType: $exerciseType
  ) {
    exercise {
        id
        name
        description
        exerciseType
    }
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


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_create_exercise(graphql_client: Client) -> None:
    """
    Given I am a developer
    When I create an exercise and I ask it back
    Then I get the created exercise back
    """
    response = graphql_client.execute(
        CREATE_EXERCISE,
        variable_values={
            'name': 'sample exercise name 0',
            'description': 'sample exercise description 0',
            'exerciseType': 'WORK',
        },
    )
    assert ERRORS not in response
    assert response['data'] == {
        'createExercise': {
            'exercise': {
                'id': '1',
                'name': 'sample exercise name 0',
                'description': 'sample exercise description 0',
                'exerciseType': 'WORK',
            },
        },
    }
