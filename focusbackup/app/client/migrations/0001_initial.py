# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('agent', models.FileField(null=True, upload_to=b'versions/agents/')),
                ('updater', models.FileField(null=True, upload_to=b'versions/updaters/')),
                ('installer', models.FileField(null=True, upload_to=b'versions/installers/')),
                ('current_agent', models.BooleanField(default=False)),
                ('current_updater', models.BooleanField(default=False)),
                ('current_installer', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model,),
        ),
    ]
