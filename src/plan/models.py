from django.db import models


class Exercise(models.Model):
    name = models.TextField(null=False)
    description = models.TextField(default="")
    # type = # use DjangoChoicesEnum, from django_graphene

    def __repr__(self) -> str:
        return f"<Exercise '{self.name}' #{self.id}>"


class Goal(models.Model):
    loop = models.ForeignKey(
        "Loop", related_name="+", on_delete=models.CASCADE
    )
    exercise = models.ForeignKey(
        Exercise, related_name="+", on_delete=models.CASCADE
    )
    entry_index = models.IntegerField(
        null=False
    )  # use MinValueValidator... entry_index >= 0
    duration = models.IntegerField()  # use MinValueValidator... duration > 0
    repetitions = (
        models.IntegerField()
    )  # use MinValueValidator... duration > 0
    description = models.TextField(default="")

    def __repr__(self) -> str:
        return f"<Goal #{self.id}>"


class Loop(models.Model):
    plan = models.ForeignKey(
        "Plan", related_name="+", on_delete=models.CASCADE
    )
    rounds = models.IntegerField(
        null=False, default=1
    )  # use MinValueValidator... rounds > 0
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


# class ExerciseType():
#     NA = 'Na'
#     TOP = 'Top'
#     MIDDLE = 'Middle'
#     BOTTOM = 'Bottom'
