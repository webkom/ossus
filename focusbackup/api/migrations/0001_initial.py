# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('api_token', models.CharField(default=b'ee76a5d05d0582202e56acd3fb9d00662a018551', max_length=40, editable=False)),
                ('active', models.BooleanField(default=True, verbose_name=b'Is token active')),
                ('api_user', models.OneToOneField(related_name='api_tokens', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
