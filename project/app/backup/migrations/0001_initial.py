# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Machine'
        db.create_table('backup_machine', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('machine_id', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('last_connection_to_client', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('backup', ['Machine'])

        # Adding model 'FolderTask'
        db.create_table('backup_foldertask', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('local_folder_path', self.gf('django.db.models.fields.TextField')()),
            ('schedule_backup', self.gf('django.db.models.fields.related.ForeignKey')(related_name='folder_tasks', to=orm['backup.ScheduleBackup'])),
        ))
        db.send_create_signal('backup', ['FolderTask'])

        # Adding model 'ScheduleBackup'
        db.create_table('backup_schedulebackup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(related_name='schedules', to=orm['backup.Machine'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('from_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('current_day_in_loop', self.gf('django.db.models.fields.IntegerField')()),
            ('days_to_keep_backups', self.gf('django.db.models.fields.IntegerField')()),
            ('last_run_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('ftp_host', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('ftp_username', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('ftp_password', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('ftp_folder', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('repeat_every_minute', self.gf('django.db.models.fields.IntegerField')()),
            ('running_backup', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('running_restore', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('backup', ['ScheduleBackup'])

        # Adding model 'Backup'
        db.create_table('backup_backup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(related_name='backups', to=orm['backup.Machine'])),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(related_name='backups', null=True, to=orm['backup.ScheduleBackup'])),
            ('time_started', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('backup', ['Backup'])


    def backwards(self, orm):
        
        # Deleting model 'Machine'
        db.delete_table('backup_machine')

        # Deleting model 'FolderTask'
        db.delete_table('backup_foldertask')

        # Deleting model 'ScheduleBackup'
        db.delete_table('backup_schedulebackup')

        # Deleting model 'Backup'
        db.delete_table('backup_backup')


    models = {
        'backup.backup': {
            'Meta': {'object_name': 'Backup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'backups'", 'to': "orm['backup.Machine']"}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'backups'", 'null': 'True', 'to': "orm['backup.ScheduleBackup']"}),
            'time_started': ('django.db.models.fields.DateTimeField', [], {})
        },
        'backup.foldertask': {
            'Meta': {'object_name': 'FolderTask'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_folder_path': ('django.db.models.fields.TextField', [], {}),
            'schedule_backup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'folder_tasks'", 'to': "orm['backup.ScheduleBackup']"})
        },
        'backup.machine': {
            'Meta': {'object_name': 'Machine'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_connection_to_client': ('django.db.models.fields.DateTimeField', [], {}),
            'machine_id': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'backup.schedulebackup': {
            'Meta': {'object_name': 'ScheduleBackup'},
            'current_day_in_loop': ('django.db.models.fields.IntegerField', [], {}),
            'days_to_keep_backups': ('django.db.models.fields.IntegerField', [], {}),
            'from_date': ('django.db.models.fields.DateTimeField', [], {}),
            'ftp_folder': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ftp_host': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'ftp_password': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'ftp_username': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_run_time': ('django.db.models.fields.DateTimeField', [], {}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'schedules'", 'to': "orm['backup.Machine']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'repeat_every_minute': ('django.db.models.fields.IntegerField', [], {}),
            'running_backup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'running_restore': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['backup']
