# Development set up

```shell
make set-up
```

## GraphiQL

Run the app (`make run`) and navigate to http://localhost:8000/graphiql.

```graphql
query {
  sessions {
    name
    description
    records {
      start
      end
      exercise {
        id
        name
      }
    }
  }
  plans {
    id
    name
    description
    loops {
      loopIndex
			rounds
      description
      goals {
        goalIndex
        exercise {
          id
          name
          description
        }
        duration
      }
    }
  }
  exercises {
    id
    name
    description
  }
  exercise(exerciseId: "1") {
    id
    name
    description
  }
}
```

Create a session:

```graphql
mutation thisIsAnOptionalNameForTheMutation {
  $name: String!,
  $start: DateTime!,
  $records: [RecordInput]!
) {
  createSession(name: $name, start: $start, records: $records) {
    session {
      name
      description
      notes
      start
      records {
        start
        end
        exercise {
          id
        }
      }
    }
  }
}
```

variables:

```json
{
  "name": "broken session",
  "start": "2020-02-21T11:03:19.337763+00:00",
  "records": [
    {
      "exerciseId": "1",
      "reps": 10,
      "start": "2020-02-23T11:03:19.325868+00:00",
      "end": "2020-02-23T11:03:19.335990+00:00"
    }
  ]
}
```

## Testing

Development testing: `make test-dev`

  - Run only tests marked with the `@pytest.mark.focus` custom decorator
  - Start `ipdb` on error.
  - See `Makefile` for more info.
