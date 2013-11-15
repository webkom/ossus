# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Machine'
        db.create_table(u'machine_machine', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='machines', to=orm['customer.Customer'])),
            ('run_install', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_connection_to_client', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 23, 0, 0), null=True, blank=True)),
            ('external_ip', self.gf('django.db.models.fields.IPAddressField')(default='', max_length=15)),
            ('local_temp_folder', self.gf('django.db.models.fields.CharField')(default='C:\\focus24\\temp\\', max_length=255)),
            ('agent_folder', self.gf('django.db.models.fields.CharField')(default='C:\\focus24\\', max_length=255)),
            ('mysql_dump', self.gf('django.db.models.fields.CharField')(default='mysqldump', max_length=255)),
            ('auto_version', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('current_agent_version', self.gf('django.db.models.fields.related.ForeignKey')(related_name='agent_versions', null=True, to=orm['client.ClientVersion'])),
            ('current_updater_version', self.gf('django.db.models.fields.related.ForeignKey')(related_name='updater_versions', null=True, to=orm['client.ClientVersion'])),
            ('selected_agent_version', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='agent_selected', null=True, to=orm['client.ClientVersion'])),
            ('selected_updater_version', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='updater_selected', null=True, to=orm['client.ClientVersion'])),
        ))
        db.send_create_signal(u'machine', ['Machine'])

        # Adding model 'MachineStats'
        db.create_table(u'machine_machinestats', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 23, 0, 0))),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stats', to=orm['machine.Machine'])),
            ('load_average', self.gf('django.db.models.fields.DecimalField')(max_digits=50, decimal_places=3)),
            ('cpu_system', self.gf('django.db.models.fields.DecimalField')(max_digits=50, decimal_places=3)),
            ('cpu_user', self.gf('django.db.models.fields.DecimalField')(max_digits=50, decimal_places=3)),
            ('cpu_stolen', self.gf('django.db.models.fields.DecimalField')(max_digits=50, decimal_places=3)),
            ('mem_used', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=50, decimal_places=3)),
            ('mem_free', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=50, decimal_places=3)),
        ))
        db.send_create_signal(u'machine', ['MachineStats'])

        # Adding model 'MachineProcessStats'
        db.create_table(u'machine_machineprocessstats', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 23, 0, 0))),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['machine.Machine'])),
            ('pid', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('cpu_usage', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=3)),
            ('mem_usage', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=3)),
        ))
        db.send_create_signal(u'machine', ['MachineProcessStats'])

        # Adding model 'MachineLog'
        db.create_table(u'machine_machinelog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(related_name='logs', to=orm['machine.Machine'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'machine', ['MachineLog'])


    def backwards(self, orm):
        # Deleting model 'Machine'
        db.delete_table(u'machine_machine')

        # Deleting model 'MachineStats'
        db.delete_table(u'machine_machinestats')

        # Deleting model 'MachineProcessStats'
        db.delete_table(u'machine_machineprocessstats')

        # Deleting model 'MachineLog'
        db.delete_table(u'machine_machinelog')


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
        u'machine.machinelog': {
            'Meta': {'object_name': 'MachineLog'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'logs'", 'to': u"orm['machine.Machine']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'machine.machineprocessstats': {
            'Meta': {'object_name': 'MachineProcessStats'},
            'cpu_usage': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '3'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 23, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['machine.Machine']"}),
            'mem_usage': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pid': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'machine.machinestats': {
            'Meta': {'object_name': 'MachineStats'},
            'cpu_stolen': ('django.db.models.fields.DecimalField', [], {'max_digits': '50', 'decimal_places': '3'}),
            'cpu_system': ('django.db.models.fields.DecimalField', [], {'max_digits': '50', 'decimal_places': '3'}),
            'cpu_user': ('django.db.models.fields.DecimalField', [], {'max_digits': '50', 'decimal_places': '3'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 23, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'load_average': ('django.db.models.fields.DecimalField', [], {'max_digits': '50', 'decimal_places': '3'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats'", 'to': u"orm['machine.Machine']"}),
            'mem_free': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '50', 'decimal_places': '3'}),
            'mem_used': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '50', 'decimal_places': '3'})
        }
    }

    complete_apps = ['machine']