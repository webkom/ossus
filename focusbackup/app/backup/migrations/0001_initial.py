# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Schedule'
        db.create_table(u'backup_schedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(related_name='backup_schedules', to=orm['machine.Machine'])),
            ('storage', self.gf('django.db.models.fields.related.ForeignKey')(related_name='backup_schedules', to=orm['storage.Storage'])),
            ('from_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_run_time', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
            ('current_version_in_loop', self.gf('django.db.models.fields.IntegerField')(default=1, blank=True)),
            ('versions_count', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('repeat_every_minute', self.gf('django.db.models.fields.IntegerField')(default=360)),
            ('running_backup', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('running_restore', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'backup', ['Schedule'])

        # Adding model 'Backup'
        db.create_table(u'backup_backup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(related_name='schedules', to=orm['machine.Machine'])),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(related_name='schedules', null=True, to=orm['backup.Schedule'])),
            ('time_started', self.gf('django.db.models.fields.DateTimeField')()),
            ('time_ended', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('day_folder_path', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
        ))
        db.send_create_signal(u'backup', ['Backup'])

        # Adding model 'Folder'
        db.create_table(u'backup_folder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(related_name='folders', to=orm['backup.Schedule'])),
            ('local_folder_path', self.gf('django.db.models.fields.TextField')()),
            ('skip_hidden_folders', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'backup', ['Folder'])

        # Adding model 'SQL'
        db.create_table(u'backup_sql', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sql_backups', to=orm['backup.Schedule'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('host', self.gf('django.db.models.fields.TextField')()),
            ('port', self.gf('django.db.models.fields.TextField')()),
            ('database', self.gf('django.db.models.fields.TextField')()),
            ('username', self.gf('django.db.models.fields.TextField')()),
            ('password', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'backup', ['SQL'])


    def backwards(self, orm):
        # Deleting model 'Schedule'
        db.delete_table(u'backup_schedule')

        # Deleting model 'Backup'
        db.delete_table(u'backup_backup')

        # Deleting model 'Folder'
        db.delete_table(u'backup_folder')

        # Deleting model 'SQL'
        db.delete_table(u'backup_sql')


    models = {
        u'accounts.company': {
            'Meta': {'object_name': 'Company'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'companies'", 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'backup.backup': {
            'Meta': {'object_name': 'Backup'},
            'day_folder_path': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'schedules'", 'to': u"orm['machine.Machine']"}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'schedules'", 'null': 'True', 'to': u"orm['backup.Schedule']"}),
            'time_ended': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'time_started': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'backup.folder': {
            'Meta': {'object_name': 'Folder'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_folder_path': ('django.db.models.fields.TextField', [], {}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'folders'", 'to': u"orm['backup.Schedule']"}),
            'skip_hidden_folders': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'backup.schedule': {
            'Meta': {'object_name': 'Schedule'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'current_version_in_loop': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'}),
            'from_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_run_time': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'backup_schedules'", 'to': u"orm['machine.Machine']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'repeat_every_minute': ('django.db.models.fields.IntegerField', [], {'default': '360'}),
            'running_backup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'running_restore': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'storage': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'backup_schedules'", 'to': u"orm['storage.Storage']"}),
            'versions_count': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        u'backup.sql': {
            'Meta': {'object_name': 'SQL'},
            'database': ('django.db.models.fields.TextField', [], {}),
            'host': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.TextField', [], {}),
            'port': ('django.db.models.fields.TextField', [], {}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sql_backups'", 'to': u"orm['backup.Schedule']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'username': ('django.db.models.fields.TextField', [], {})
        },
        u'client.clientversion': {
            'Meta': {'object_name': 'ClientVersion'},
            'agent': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'current_agent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'current_updater': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updater': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'customer.customer': {
            'Meta': {'object_name': 'Customer'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'customers'", 'to': u"orm['accounts.Company']"}),
            'contact_email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'contact_person': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'machine.machine': {
            'Meta': {'object_name': 'Machine'},
            'agent_folder': ('django.db.models.fields.CharField', [], {'default': "'C:\\\\focus24\\\\'", 'max_length': '255'}),
            'auto_version': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'current_agent_version': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'agent_versions'", 'null': 'True', 'to': u"orm['client.ClientVersion']"}),
            'current_updater_version': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'updater_versions'", 'null': 'True', 'to': u"orm['client.ClientVersion']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'machines'", 'to': u"orm['customer.Customer']"}),
            'external_ip': ('django.db.models.fields.IPAddressField', [], {'default': "''", 'max_length': '15'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_connection_to_client': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 23, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'local_temp_folder': ('django.db.models.fields.CharField', [], {'default': "'C:\\\\focus24\\\\temp\\\\'", 'max_length': '255'}),
            'mysql_dump': ('django.db.models.fields.CharField', [], {'default': "'mysqldump'", 'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'run_install': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'selected_agent_version': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'agent_selected'", 'null': 'True', 'to': u"orm['client.ClientVersion']"}),
            'selected_updater_version': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'updater_selected'", 'null': 'True', 'to': u"orm['client.ClientVersion']"})
        },
        u'storage.storage': {
            'Meta': {'object_name': 'Storage'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'storages'", 'null': 'True', 'to': u"orm['accounts.Company']"}),
            'folder': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['backup']