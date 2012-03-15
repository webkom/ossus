# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'MachineUptimeLog'
        db.delete_table('backup_machineuptimelog')

        # Deleting model 'UptimeLogBase'
        db.delete_table('backup_uptimelogbase')

        # Deleting field 'ClientVersion.current'
        db.delete_column('backup_clientversion', 'current')

        # Adding field 'ClientVersion.current_agent'
        db.add_column('backup_clientversion', 'current_agent', self.gf('django.db.models.fields.BooleanField')(default=False, unique=True), keep_default=False)

        # Adding field 'ClientVersion.current_updater'
        db.add_column('backup_clientversion', 'current_updater', self.gf('django.db.models.fields.BooleanField')(default=False, unique=True), keep_default=False)

        # Adding field 'Machine.auto_version'
        db.add_column('backup_machine', 'auto_version', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'Machine.current_agent_version'
        db.add_column('backup_machine', 'current_agent_version', self.gf('django.db.models.fields.related.ForeignKey')(related_name='agent_versions', null=True, to=orm['backup.ClientVersion']), keep_default=False)

        # Adding field 'Machine.current_updater_version'
        db.add_column('backup_machine', 'current_updater_version', self.gf('django.db.models.fields.related.ForeignKey')(related_name='updater_versions', null=True, to=orm['backup.ClientVersion']), keep_default=False)

        # Adding field 'Machine.selected_agent_version'
        db.add_column('backup_machine', 'selected_agent_version', self.gf('django.db.models.fields.related.ForeignKey')(related_name='agent_selected', null=True, to=orm['backup.ClientVersion']), keep_default=False)

        # Adding field 'Machine.selected_updater_version'
        db.add_column('backup_machine', 'selected_updater_version', self.gf('django.db.models.fields.related.ForeignKey')(related_name='updater_selected', null=True, to=orm['backup.ClientVersion']), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'MachineUptimeLog'
        db.create_table('backup_machineuptimelog', (
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(related_name='updatelogs', to=orm['backup.Machine'])),
            ('uptimelogbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['backup.UptimeLogBase'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('backup', ['MachineUptimeLog'])

        # Adding model 'UptimeLogBase'
        db.create_table('backup_uptimelogbase', (
            ('type', self.gf('django.db.models.fields.CharField')(default='up', max_length=5)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('backup', ['UptimeLogBase'])

        # Adding field 'ClientVersion.current'
        db.add_column('backup_clientversion', 'current', self.gf('django.db.models.fields.BooleanField')(default=False, unique=True), keep_default=False)

        # Deleting field 'ClientVersion.current_agent'
        db.delete_column('backup_clientversion', 'current_agent')

        # Deleting field 'ClientVersion.current_updater'
        db.delete_column('backup_clientversion', 'current_updater')

        # Deleting field 'Machine.auto_version'
        db.delete_column('backup_machine', 'auto_version')

        # Deleting field 'Machine.current_agent_version'
        db.delete_column('backup_machine', 'current_agent_version_id')

        # Deleting field 'Machine.current_updater_version'
        db.delete_column('backup_machine', 'current_updater_version_id')

        # Deleting field 'Machine.selected_agent_version'
        db.delete_column('backup_machine', 'selected_agent_version_id')

        # Deleting field 'Machine.selected_updater_version'
        db.delete_column('backup_machine', 'selected_updater_version_id')


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
            'current_agent': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'unique': 'True'}),
            'current_updater': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'unique': 'True'}),
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
        'backup.location': {
            'Meta': {'object_name': 'Location'},
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'locations'", 'to': "orm['backup.Customer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'backup.machine': {
            'Meta': {'object_name': 'Machine'},
            'auto_version': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'current_agent_version': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'agent_versions'", 'null': 'True', 'to': "orm['backup.ClientVersion']"}),
            'current_updater_version': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'updater_versions'", 'null': 'True', 'to': "orm['backup.ClientVersion']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'last_connection_to_client': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'machines'", 'to': "orm['backup.Location']"}),
            'machine_id': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'selected_agent_version': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'agent_selected'", 'null': 'True', 'to': "orm['backup.ClientVersion']"}),
            'selected_updater_version': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'updater_selected'", 'null': 'True', 'to': "orm['backup.ClientVersion']"})
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
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 3, 15, 17, 29, 50, 613529)'}),
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
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 3, 15, 17, 29, 50, 612891)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'load_average': ('django.db.models.fields.DecimalField', [], {'max_digits': '50', 'decimal_places': '3'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats'", 'to': "orm['backup.Machine']"}),
            'mem_free': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'mem_used': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'backup.schedulebackup': {
            'Meta': {'object_name': 'ScheduleBackup'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'current_version_in_loop': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
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
            'port': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
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
