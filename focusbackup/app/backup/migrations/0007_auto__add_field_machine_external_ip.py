# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Machine.external_ip'
        db.add_column('backup_machine', 'external_ip',
                      self.gf('django.db.models.fields.IPAddressField')(default='', max_length=15),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Machine.external_ip'
        db.delete_column('backup_machine', 'external_ip')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'backup.backup': {
            'Meta': {'object_name': 'Backup'},
            'day_folder_path': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'backups'", 'to': "orm['backup.Machine']"}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'backups'", 'null': 'True', 'to': "orm['backup.ScheduleBackup']"}),
            'time_ended': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'time_started': ('django.db.models.fields.DateTimeField', [], {})
        },
        'backup.clientversion': {
            'Meta': {'object_name': 'ClientVersion'},
            'agent': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'current_agent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'current_updater': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updater': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'})
        },
        'backup.company': {
            'Meta': {'object_name': 'Company'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'companies'", 'symmetrical': 'False', 'to': "orm['auth.User']"})
        },
        'backup.customer': {
            'Meta': {'object_name': 'Customer'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'customers'", 'to': "orm['backup.Company']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'backup.folderbackup': {
            'Meta': {'object_name': 'FolderBackup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_folder_path': ('django.db.models.fields.TextField', [], {}),
            'schedule_backup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'folder_backups'", 'to': "orm['backup.ScheduleBackup']"}),
            'skip_hidden_folders': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'backup.machine': {
            'Meta': {'object_name': 'Machine'},
            'auto_version': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'current_agent_version': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'agent_versions'", 'null': 'True', 'to': "orm['backup.ClientVersion']"}),
            'current_updater_version': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'updater_versions'", 'null': 'True', 'to': "orm['backup.ClientVersion']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'machines'", 'to': "orm['backup.Customer']"}),
            'external_ip': ('django.db.models.fields.IPAddressField', [], {'default': "''", 'max_length': '15'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_connection_to_client': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 10, 12, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'machine_id': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'run_install': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'selected_agent_version': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'agent_selected'", 'null': 'True', 'to': "orm['backup.ClientVersion']"}),
            'selected_updater_version': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'updater_selected'", 'null': 'True', 'to': "orm['backup.ClientVersion']"})
        },
        'backup.machinelog': {
            'Meta': {'object_name': 'MachineLog'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'logs'", 'to': "orm['backup.Machine']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'backup.machineprocessstats': {
            'Meta': {'object_name': 'MachineProcessStats'},
            'cpu_usage': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '3'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 10, 12, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backup.Machine']"}),
            'mem_usage': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pid': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'backup.machinestats': {
            'Meta': {'object_name': 'MachineStats'},
            'cpu_stolen': ('django.db.models.fields.DecimalField', [], {'max_digits': '50', 'decimal_places': '3'}),
            'cpu_system': ('django.db.models.fields.DecimalField', [], {'max_digits': '50', 'decimal_places': '3'}),
            'cpu_user': ('django.db.models.fields.DecimalField', [], {'max_digits': '50', 'decimal_places': '3'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 10, 12, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'load_average': ('django.db.models.fields.DecimalField', [], {'max_digits': '50', 'decimal_places': '3'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats'", 'to': "orm['backup.Machine']"}),
            'mem_free': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '50', 'decimal_places': '3'}),
            'mem_used': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '50', 'decimal_places': '3'})
        },
        'backup.schedulebackup': {
            'Meta': {'object_name': 'ScheduleBackup'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'current_version_in_loop': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'}),
            'from_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_run_time': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'schedules'", 'to': "orm['backup.Machine']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'repeat_every_minute': ('django.db.models.fields.IntegerField', [], {'default': '360'}),
            'running_backup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'running_restore': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'storage': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'schedules'", 'to': "orm['backup.Storage']"}),
            'versions_count': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'backup.sqlbackup': {
            'Meta': {'object_name': 'SQLBackup'},
            'database': ('django.db.models.fields.TextField', [], {}),
            'host': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.TextField', [], {}),
            'port': ('django.db.models.fields.TextField', [], {}),
            'schedule_backup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sql_backups'", 'to': "orm['backup.ScheduleBackup']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'username': ('django.db.models.fields.TextField', [], {})
        },
        'backup.storage': {
            'Meta': {'object_name': 'Storage'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'storages'", 'null': 'True', 'to': "orm['backup.Company']"}),
            'folder': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['backup']