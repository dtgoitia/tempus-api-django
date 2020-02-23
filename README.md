# Development set up

```shell
make install
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
