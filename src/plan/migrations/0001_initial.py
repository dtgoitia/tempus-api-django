# Generated by Django 3.0.3 on 2020-02-21 15:13

import django.db.models.deletion
from django.db import migrations, models


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
                        help_text='Date and time at which the session started.'
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
                        help_text='Date and time at which the execution of the exercise started.'
                    ),
                ),
                (
                    'end',
                    models.DateTimeField(
                        help_text='Date and time at which the execution of the exercise finished.'
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
                ('rounds', models.IntegerField(default=1)),
                ('loop_index', models.IntegerField()),
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
                ('entry_index', models.IntegerField()),
                ('duration', models.IntegerField(null=True)),
                ('repetitions', models.IntegerField(null=True)),
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
