# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Company'
        db.create_table('backup_company', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal('backup', ['Company'])

        # Adding M2M table for field users on 'Company'
        db.create_table('backup_company_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('company', models.ForeignKey(orm['backup.company'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('backup_company_users', ['company_id', 'user_id'])

        # Adding model 'Customer'
        db.create_table('backup_customer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(related_name='customers', to=orm['backup.Company'])),
        ))
        db.send_create_signal('backup', ['Customer'])

        # Adding model 'Machine'
        db.create_table('backup_machine', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='machines', to=orm['backup.Customer'])),
            ('machine_id', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('last_connection_to_client', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('auto_version', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('current_agent_version', self.gf('django.db.models.fields.related.ForeignKey')(related_name='agent_versions', null=True, to=orm['backup.ClientVersion'])),
            ('current_updater_version', self.gf('django.db.models.fields.related.ForeignKey')(related_name='updater_versions', null=True, to=orm['backup.ClientVersion'])),
            ('selected_agent_version', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='agent_selected', null=True, to=orm['backup.ClientVersion'])),
            ('selected_updater_version', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='updater_selected', null=True, to=orm['backup.ClientVersion'])),
        ))
        db.send_create_signal('backup', ['Machine'])

        # Adding model 'MachineStats'
        db.create_table('backup_machinestats', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 4, 9, 0, 0))),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stats', to=orm['backup.Machine'])),
            ('load_average', self.gf('django.db.models.fields.DecimalField')(max_digits=50, decimal_places=3)),
            ('cpu_system', self.gf('django.db.models.fields.DecimalField')(max_digits=50, decimal_places=3)),
            ('cpu_user', self.gf('django.db.models.fields.DecimalField')(max_digits=50, decimal_places=3)),
            ('cpu_stolen', self.gf('django.db.models.fields.DecimalField')(max_digits=50, decimal_places=3)),
            ('mem_used', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('mem_free', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('backup', ['MachineStats'])

        # Adding model 'MachineProcessStats'
        db.create_table('backup_machineprocessstats', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 4, 9, 0, 0))),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backup.Machine'])),
            ('pid', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('cpu_usage', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=3)),
            ('mem_usage', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=3)),
        ))
        db.send_create_signal('backup', ['MachineProcessStats'])

        # Adding model 'MachineLog'
        db.create_table('backup_machinelog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(related_name='logs', to=orm['backup.Machine'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('backup', ['MachineLog'])

        # Adding model 'Storage'
        db.create_table('backup_storage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(related_name='storages', null=True, to=orm['backup.Company'])),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('folder', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('backup', ['Storage'])

        # Adding model 'FolderBackup'
        db.create_table('backup_folderbackup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('local_folder_path', self.gf('django.db.models.fields.TextField')()),
            ('schedule_backup', self.gf('django.db.models.fields.related.ForeignKey')(related_name='folder_backups', to=orm['backup.ScheduleBackup'])),
            ('skip_hidden_folders', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('backup', ['FolderBackup'])

        # Adding model 'SQLBackup'
        db.create_table('backup_sqlbackup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.TextField')(max_length=40)),
            ('schedule_backup', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sql_backups', to=orm['backup.ScheduleBackup'])),
            ('host', self.gf('django.db.models.fields.TextField')()),
            ('port', self.gf('django.db.models.fields.TextField')()),
            ('database', self.gf('django.db.models.fields.TextField')()),
            ('username', self.gf('django.db.models.fields.TextField')()),
            ('password', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('backup', ['SQLBackup'])

        # Adding model 'ScheduleBackup'
        db.create_table('backup_schedulebackup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(related_name='schedules', to=orm['backup.Machine'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('storage', self.gf('django.db.models.fields.related.ForeignKey')(related_name='schedules', to=orm['backup.Storage'])),
            ('from_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_run_time', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
            ('current_version_in_loop', self.gf('django.db.models.fields.IntegerField')(default=1, blank=True)),
            ('versions_count', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('repeat_every_minute', self.gf('django.db.models.fields.IntegerField')(default=360)),
            ('running_backup', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('running_restore', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('backup', ['ScheduleBackup'])

        # Adding model 'Backup'
        db.create_table('backup_backup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(related_name='backups', to=orm['backup.Machine'])),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(related_name='backups', null=True, to=orm['backup.ScheduleBackup'])),
            ('time_started', self.gf('django.db.models.fields.DateTimeField')()),
            ('time_ended', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('day_folder_path', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
        ))
        db.send_create_signal('backup', ['Backup'])

        # Adding model 'ClientVersion'
        db.create_table('backup_clientversion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('agent_link', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('updater_link', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('current_agent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('current_updater', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('backup', ['ClientVersion'])

    def backwards(self, orm):
        # Deleting model 'Company'
        db.delete_table('backup_company')

        # Removing M2M table for field users on 'Company'
        db.delete_table('backup_company_users')

        # Deleting model 'Customer'
        db.delete_table('backup_customer')

        # Deleting model 'Machine'
        db.delete_table('backup_machine')

        # Deleting model 'MachineStats'
        db.delete_table('backup_machinestats')

        # Deleting model 'MachineProcessStats'
        db.delete_table('backup_machineprocessstats')

        # Deleting model 'MachineLog'
        db.delete_table('backup_machinelog')

        # Deleting model 'Storage'
        db.delete_table('backup_storage')

        # Deleting model 'FolderBackup'
        db.delete_table('backup_folderbackup')

        # Deleting model 'SQLBackup'
        db.delete_table('backup_sqlbackup')

        # Deleting model 'ScheduleBackup'
        db.delete_table('backup_schedulebackup')

        # Deleting model 'Backup'
        db.delete_table('backup_backup')

        # Deleting model 'ClientVersion'
        db.delete_table('backup_clientversion')

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
            'agent_link': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'current_agent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'current_updater': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updater_link': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_connection_to_client': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'machine_id': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
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
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 4, 9, 0, 0)'}),
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
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 4, 9, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'load_average': ('django.db.models.fields.DecimalField', [], {'max_digits': '50', 'decimal_places': '3'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats'", 'to': "orm['backup.Machine']"}),
            'mem_free': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'mem_used': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
            'type': ('django.db.models.fields.TextField', [], {'max_length': '40'}),
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