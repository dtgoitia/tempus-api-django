from django.db import models


class Exercise(models.Model):
    name = models.TextField(null=False)
    description = models.TextField(default="")
    # type = # use DjangoChoicesEnum, from django_graphene

    def __repr__(self) -> str:
        return f"<Exercise '{self.name}' #{self.id}>"


class Goal(models.Model):
    loop = models.ForeignKey(
        "Loop", on_delete=models.CASCADE, related_name="goals",
    )
    exercise = models.ForeignKey(
        Exercise, related_name="+", on_delete=models.CASCADE
    )
    # TODO: rename to goal_index
    # TODO: add helper text 'position of the goal inside the loop'
    entry_index = models.IntegerField(
        null=False
    )  # use MinValueValidator... entry_index >= 0
    duration = models.IntegerField(
        null=True
    )  # use MinValueValidator... duration > 0
    # use MinValueValidator... duration > 0
    repetitions = models.IntegerField(null=True)

    # TODO: I don't think a description is needed fot the goals... the Exercise
    # itself should contain all the info related to how to do the exercise, etc
    # so I don't what value can the Goal description add
    description = models.TextField(default="")

    def __repr__(self) -> str:
        return f"<Goal #{self.id}>"


class Loop(models.Model):
    plan = models.ForeignKey(
        "Plan", on_delete=models.CASCADE, related_name="loops",
    )
    rounds = models.IntegerField(
        null=False, default=1
    )  # use MinValueValidator... rounds > 0
    # TODO: add helper text 'position of the loop inside the plan'
    loop_index = models.IntegerField(
        null=False
    )  # use MinValueValidator... loop_index >= 0
    description = models.TextField(default="")

    def __repr__(self) -> str:
        return f"<Loop #{self.id}>"


class Plan(models.Model):
    name = models.TextField(null=False)
    description = models.TextField(default="")

    def __repr__(self) -> str:
        return f"<Plan '{self.name}'>"


class Session(models.Model):
    name = models.TextField(
        null=False, help_text='Short name for the user to identify the session'
    )
    description = models.TextField(
        default="",
        help_text='Short description for the user to get a better understanding of what the session is about',
    )
    notes = models.TextField(
        default="",
        help_text='Optional space for notes like: what went well/bad, injuries, why the session was aborted...',
    )

    # The start time of the session and the start time of the first record
    # might differ, e.g.: the user starts a session, goes to prepare material,
    # and then starts executing exercises - there is a time gap between the
    # session start and the first executed exercise start.
    # auto_now=False because the time will be recorded by the client, which
    # could be communicated hours later to the server
    # TODO: validation - 'start' cannot be in the future
    start = models.DateTimeField(
        auto_now=False,
        null=False,
        help_text='Date and time at which the session started.',
    )

    def __repr__(self) -> str:
        return f"<Session '{self.name}'>"


class Record(models.Model):
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name='records', null=False
    )
    exercise = models.ForeignKey(
        Exercise, on_delete=models.CASCADE, related_name='+', null=False
    )

    # auto_now=False because the time will be recorded by the client, which
    # could be communicated hours later to the server
    # TODO: validation - 'start' cannot be in the future
    start = models.DateTimeField(
        auto_now=False,
        null=False,
        help_text='Date and time at which the execution of the exercise started.',
    )
    # auto_now=False because the time will be recorded by the client, which
    # could be communicated hours later to the server
    # TODO: validation - 'end' cannot be in the future
    end = models.DateTimeField(
        auto_now=False,
        null=False,
        help_text='Date and time at which the execution of the exercise finished.',
    )

    def __repr__(self) -> str:
        return f"<Record '{self.exercise.name}'>"


# class ExerciseType():
#     NA = 'Na'
#     TOP = 'Top'
#     MIDDLE = 'Middle'
#     BOTTOM = 'Bottom'
