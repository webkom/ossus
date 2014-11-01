# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=10, choices=[(b'ftp', b'FTP')])),
                ('name', models.CharField(default=b'', max_length=100)),
                ('notes', models.TextField(default=b'')),
                ('host', models.CharField(max_length=150)),
                ('username', models.CharField(max_length=80)),
                ('password', models.CharField(max_length=80)),
                ('folder', models.CharField(max_length=255)),
                ('company', models.ForeignKey(related_name='storages', to='accounts.Company', null=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
    ]
