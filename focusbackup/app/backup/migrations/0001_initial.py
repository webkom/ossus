# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0001_initial'),
        ('machine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Backup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_started', models.DateTimeField()),
                ('time_ended', models.DateTimeField(null=True, blank=True)),
                ('day_folder_path', models.CharField(max_length=150, blank=True)),
                ('file_name', models.CharField(max_length=150, null=True, blank=True)),
                ('machine', models.ForeignKey(related_name='backups', to='machine.Machine')),
            ],
            options={
                'ordering': ['-id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('local_folder_path', models.TextField()),
                ('skip_hidden_folders', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('from_date', models.DateTimeField()),
                ('last_run_time', models.DateTimeField(default=None, null=True)),
                ('current_version_in_loop', models.IntegerField(default=1, blank=True)),
                ('versions_count', models.IntegerField(default=10, verbose_name=b'Number of copies')),
                ('repeat_every_minute', models.IntegerField(default=360, choices=[(5, b'Hvert 5 min'), (10, b'Hvert 10 min'), (15, b'Hvert kvarter'), (60, b'Hver time'), (180, b'Hver tredje time'), (1440, b'Hver dag'), (2880, b'Hver andre dag'), (4320, b'Hver tredje dag'), (10080, b'Hver uke'), (43829, b'Hver m\xc3\xa5ned')])),
                ('running_backup', models.BooleanField(default=False)),
                ('running_restore', models.BooleanField(default=False)),
                ('run_now', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('machine', models.ForeignKey(related_name='schedules', to='machine.Machine')),
                ('storage', models.ForeignKey(related_name='schedules', to='storage.Storage')),
            ],
            options={
                'ordering': ['name', 'id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SQL',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=40, choices=[(b'', b'Velg'), (b'mysql', b'MySQL'), (b'mssql', b'MSSQL')])),
                ('host', models.TextField()),
                ('port', models.TextField()),
                ('database', models.TextField()),
                ('username', models.TextField()),
                ('password', models.TextField()),
                ('schedule', models.ForeignKey(related_name='sql_backups', to='backup.Schedule', null=True)),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='folder',
            name='schedule',
            field=models.ForeignKey(related_name='folders', to='backup.Schedule', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='backup',
            name='schedule',
            field=models.ForeignKey(related_name='backups', to='backup.Schedule', null=True),
            preserve_default=True,
        ),
    ]
