# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('run_install', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=True)),
                ('template', models.BooleanField(default=False)),
                ('external_ip', models.IPAddressField(default=b'')),
                ('local_temp_folder', models.CharField(default=b'C:\\focus24\\temp\\', max_length=255)),
                ('agent_folder', models.CharField(default=b'C:\\focus24\\', max_length=255)),
                ('mysql_dump', models.CharField(default=b'mysqldump', max_length=255)),
                ('auto_version', models.BooleanField(default=True)),
                ('lock', models.DateTimeField(default=None, null=True, blank=True)),
                ('lock_session', models.CharField(default=None, max_length=255, null=True)),
                ('current_agent_version', models.ForeignKey(related_name='agent_versions', to='client.ClientVersion', null=True)),
                ('current_updater_version', models.ForeignKey(related_name='updater_versions', to='client.ClientVersion', null=True)),
                ('customer', models.ForeignKey(related_name='machines', to='customer.Customer')),
                ('selected_agent_version', models.ForeignKey(related_name='agent_selected', blank=True, to='client.ClientVersion', null=True)),
                ('selected_updater_version', models.ForeignKey(related_name='updater_selected', blank=True, to='client.ClientVersion', null=True)),
            ],
            options={
                'ordering': ['-active', 'name', 'id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MachineLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField()),
                ('text', models.TextField()),
                ('type', models.CharField(max_length=10, choices=[(b'info', b'INFO'), (b'error', b'ERROR'), (b'warning', b'WARNING')])),
                ('machine', models.ForeignKey(related_name='logs', to='machine.Machine')),
            ],
            options={
                'ordering': ['-id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MachineProcessStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(default=datetime.datetime(2014, 11, 1, 13, 16, 58, 992234))),
                ('pid', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('user', models.CharField(max_length=100)),
                ('cpu_usage', models.DecimalField(max_digits=10, decimal_places=3)),
                ('mem_usage', models.DecimalField(max_digits=10, decimal_places=3)),
                ('machine', models.ForeignKey(to='machine.Machine')),
            ],
            options={
                'ordering': ['-id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MachineStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(default=datetime.datetime(2014, 11, 1, 13, 16, 58, 991493))),
                ('load_average', models.DecimalField(max_digits=50, decimal_places=3)),
                ('cpu_system', models.DecimalField(max_digits=50, decimal_places=3)),
                ('cpu_user', models.DecimalField(max_digits=50, decimal_places=3)),
                ('cpu_stolen', models.DecimalField(max_digits=50, decimal_places=3)),
                ('mem_used', models.DecimalField(default=0, max_digits=50, decimal_places=3)),
                ('mem_free', models.DecimalField(default=0, max_digits=50, decimal_places=3)),
                ('machine', models.ForeignKey(related_name='stats', to='machine.Machine')),
            ],
            options={
                'ordering': ['-id'],
            },
            bases=(models.Model,),
        ),
    ]
