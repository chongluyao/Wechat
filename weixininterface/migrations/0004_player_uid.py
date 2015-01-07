# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weixininterface', '0003_auto_20141224_0040'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='uid',
            field=models.CharField(default=b'anonymity', max_length=255),
            preserve_default=True,
        ),
    ]
