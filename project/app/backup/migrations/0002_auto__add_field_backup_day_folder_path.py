# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Backup.day_folder_path'
        db.add_column('backup_backup', 'day_folder_path', self.gf('django.db.models.fields.CharField')(default='', max_length=150), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Backup.day_folder_path'
        db.delete_column('backup_backup', 'day_folder_path')


    models = {
        'backup.backup': {
            'Meta': {'object_name': 'Backup'},
            'day_folder_path': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
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
