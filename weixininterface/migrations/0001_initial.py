# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('exercise_num', models.IntegerField(default=0)),
                ('introduction', models.CharField(default=b'no introduction', max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CoursesRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0)),
                ('course', models.ForeignKey(to='weixininterface.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(default=b'anonymity', max_length=255)),
                ('state', models.IntegerField(default=0)),
                ('current_score', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(default=b'question', max_length=255)),
                ('choice1', models.CharField(default=b'choice1', max_length=255)),
                ('choice2', models.CharField(default=b'choice2', max_length=255)),
                ('choice3', models.CharField(default=b'choice3', max_length=255)),
                ('choice4', models.CharField(default=b'choice4', max_length=255)),
                ('answer', models.IntegerField(default=0)),
                ('answer_times', models.IntegerField(default=0)),
                ('answer_correct_times', models.IntegerField(default=0)),
                ('contributor', models.CharField(default=b'children', max_length=255)),
                ('course', models.ForeignKey(to='weixininterface.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionsRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.IntegerField()),
                ('player', models.ForeignKey(to='weixininterface.Player')),
                ('question', models.ForeignKey(to='weixininterface.Question')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='player',
            name='current_question',
            field=models.ForeignKey(to='weixininterface.Question', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coursesrecord',
            name='player',
            field=models.ForeignKey(to='weixininterface.Player'),
            preserve_default=True,
        ),
    ]
