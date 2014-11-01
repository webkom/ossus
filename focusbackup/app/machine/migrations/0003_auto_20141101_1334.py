# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('machine', '0002_auto_20141101_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machineprocessstats',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 1, 13, 34, 34, 708621)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='machinestats',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 1, 13, 34, 34, 707688)),
            preserve_default=True,
        ),
    ]
