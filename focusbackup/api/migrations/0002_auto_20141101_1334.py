# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='api_token',
            field=models.CharField(default=b'294465c7061779b83db2888ee17b839dfdc8c9fe', max_length=40, editable=False),
            preserve_default=True,
        ),
    ]
