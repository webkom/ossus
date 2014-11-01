# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('address', models.CharField(max_length=100, null=True, blank=True)),
                ('contact_person', models.CharField(max_length=100, null=True, blank=True)),
                ('contact_email', models.CharField(max_length=100, null=True, blank=True)),
                ('contact_phone', models.CharField(max_length=20, null=True, blank=True)),
                ('company', models.ForeignKey(related_name='customers', to='accounts.Company')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
    ]
