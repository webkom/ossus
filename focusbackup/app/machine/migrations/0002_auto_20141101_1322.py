# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('machine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machineprocessstats',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 1, 13, 22, 15, 925954)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='machinestats',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 1, 13, 22, 15, 925201)),
            preserve_default=True,
        ),
    ]
