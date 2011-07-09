# encoding: utf-8
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

        # Adding model 'Location'
        db.create_table('backup_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='locations', to=orm['backup.Customer'])),
        ))
        db.send_create_signal('backup', ['Location'])

        # Adding model 'Machine'
        db.create_table('backup_machine', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='machines', to=orm['backup.Location'])),
            ('machine_id', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('last_connection_to_client', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
        ))
        db.send_create_signal('backup', ['Machine'])

        # Adding model 'Storage'
        db.create_table('backup_storage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
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
        ))
        db.send_create_signal('backup', ['FolderBackup'])

        # Adding model 'SQLBackup'
        db.create_table('backup_sqlbackup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('schedule_backup', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sql_backups', to=orm['backup.ScheduleBackup'])),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('database', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('backup', ['SQLBackup'])

        # Adding model 'ScheduleBackup'
        db.create_table('backup_schedulebackup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(related_name='schedules', to=orm['backup.Machine'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('storage', self.gf('django.db.models.fields.related.ForeignKey')(related_name='schedules', to=orm['backup.Storage'])),
            ('from_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_run_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('current_day_in_loop', self.gf('django.db.models.fields.IntegerField')()),
            ('versions_count', self.gf('django.db.models.fields.IntegerField')()),
            ('repeat_every_minute', self.gf('django.db.models.fields.IntegerField')()),
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
            ('day_folder_path', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
        ))
        db.send_create_signal('backup', ['Backup'])


    def backwards(self, orm):
        
        # Deleting model 'Company'
        db.delete_table('backup_company')

        # Removing M2M table for field users on 'Company'
        db.delete_table('backup_company_users')

        # Deleting model 'Customer'
        db.delete_table('backup_customer')

        # Deleting model 'Location'
        db.delete_table('backup_location')

        # Deleting model 'Machine'
        db.delete_table('backup_machine')

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
            'time_started': ('django.db.models.fields.DateTimeField', [], {})
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
            'schedule_backup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'folder_backups'", 'to': "orm['backup.ScheduleBackup']"})
        },
        'backup.location': {
            'Meta': {'object_name': 'Location'},
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'locations'", 'to': "orm['backup.Customer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'backup.machine': {
            'Meta': {'object_name': 'Machine'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'last_connection_to_client': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'machines'", 'to': "orm['backup.Location']"}),
            'machine_id': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'backup.schedulebackup': {
            'Meta': {'object_name': 'ScheduleBackup'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'current_day_in_loop': ('django.db.models.fields.IntegerField', [], {}),
            'from_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_run_time': ('django.db.models.fields.DateTimeField', [], {}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'schedules'", 'to': "orm['backup.Machine']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'repeat_every_minute': ('django.db.models.fields.IntegerField', [], {}),
            'running_backup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'running_restore': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'storage': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'schedules'", 'to': "orm['backup.Storage']"}),
            'versions_count': ('django.db.models.fields.IntegerField', [], {})
        },
        'backup.sqlbackup': {
            'Meta': {'object_name': 'SQLBackup'},
            'database': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'schedule_backup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sql_backups'", 'to': "orm['backup.ScheduleBackup']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'backup.storage': {
            'Meta': {'object_name': 'Storage'},
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
