# Generated by Django 3.0.3 on 2020-02-22 22:45

import django.db.models.deletion
from django.db import migrations, models

import src.plan.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.TextField()),
                ('description', models.TextField(default='')),
                (
                    'type',
                    models.CharField(
                        choices=[
                            ('WORK', 'Work'),
                            ('REST', 'Rest'),
                            ('PREP', 'Preparation'),
                        ],
                        max_length=4,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.TextField()),
                ('description', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.TextField(
                        help_text='Short name for the user to identify the session'
                    ),
                ),
                (
                    'description',
                    models.TextField(
                        default='',
                        help_text='Short description for the user to get a better understanding of what the session is about',
                    ),
                ),
                (
                    'notes',
                    models.TextField(
                        default='',
                        help_text='Optional space for notes like: what went well/bad, injuries, why the session was aborted...',
                    ),
                ),
                (
                    'start',
                    models.DateTimeField(
                        help_text='Date and time at which the session started.',
                        validators=[src.plan.models.is_not_future_datetime],
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'start',
                    models.DateTimeField(
                        help_text='Date and time at which the execution of the exercise started.',
                        validators=[src.plan.models.is_not_future_datetime],
                    ),
                ),
                (
                    'end',
                    models.DateTimeField(
                        help_text='Date and time at which the execution of the exercise finished.',
                        validators=[src.plan.models.is_not_future_datetime],
                    ),
                ),
                (
                    'exercise',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='+',
                        to='plan.Exercise',
                    ),
                ),
                (
                    'session',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='records',
                        to='plan.Session',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Loop',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'rounds',
                    models.IntegerField(
                        default=1,
                        help_text='amount of times that the whole block of Goals under the Loop will be executed',
                        validators=[src.plan.models.is_positive_number],
                    ),
                ),
                (
                    'loop_index',
                    models.IntegerField(
                        help_text='position of the Loop inside the parent Plan',
                        validators=[src.plan.models.is_positive_number],
                    ),
                ),
                ('description', models.TextField(default='')),
                (
                    'plan',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='loops',
                        to='plan.Plan',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'goal_index',
                    models.IntegerField(
                        help_text='position of the Goal inside the parent Loop',
                        validators=[src.plan.models.is_positive_number],
                    ),
                ),
                (
                    'duration',
                    models.IntegerField(
                        help_text='time allocated to execute the Exercise',
                        null=True,
                        validators=[src.plan.models.is_positive_number],
                    ),
                ),
                (
                    'repetitions',
                    models.IntegerField(
                        help_text='amount of times the Exercise needs to be repeated during a single execution',
                        null=True,
                        validators=[src.plan.models.is_positive_number],
                    ),
                ),
                (
                    'pause',
                    models.BooleanField(
                        default=False,
                        help_text='specifies if the goal waits for users approval to run or not',
                    ),
                ),
                ('description', models.TextField(default='')),
                (
                    'exercise',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='+',
                        to='plan.Exercise',
                    ),
                ),
                (
                    'loop',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='goals',
                        to='plan.Loop',
                    ),
                ),
            ],
        ),
    ]

