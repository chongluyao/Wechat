# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weixininterface', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='current_question',
        ),
        migrations.RemoveField(
            model_name='player',
            name='current_score',
        ),
        migrations.AlterField(
            model_name='player',
            name='state',
            field=models.CharField(default=b'none', max_length=255),
            preserve_default=True,
        ),
    ]
