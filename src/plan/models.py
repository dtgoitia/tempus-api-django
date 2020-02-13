from django.db import models


class Plan(models.Model):
    name = models.TextField(null=False)
    description = models.TextField(default="")


class Loop(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    rounds = models.IntegerField(
        null=False, default=1
    )  # use MinValueValidator... rounds > 0
    loop_index = models.IntegerField(
        null=False
    )  # use MinValueValidator... loop_index >= 0
    description = models.TextField(default="")


class Exercise(models.Model):
    name = models.TextField(null=False)
    description = models.TextField(default="")
    # type = # use DjangoChoicesEnum, from django_graphene


class Goal(models.Model):
    loop = models.ForeignKey(Loop, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    entry_index = models.IntegerField(
        null=False
    )  # use MinValueValidator... entry_index >= 0
    duration = models.IntegerField()  # use MinValueValidator... duration > 0
    repetitions = (
        models.IntegerField()
    )  # use MinValueValidator... duration > 0
    description = models.TextField(default="")


# class ExerciseType():
#     NA = 'Na'
#     TOP = 'Top'
#     MIDDLE = 'Middle'
#     BOTTOM = 'Bottom'
