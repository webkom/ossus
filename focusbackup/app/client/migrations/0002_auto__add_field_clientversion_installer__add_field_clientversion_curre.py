# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ClientVersion.installer'
        db.add_column(u'client_clientversion', 'installer',
                      self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True),
                      keep_default=False)

        # Adding field 'ClientVersion.current_installer'
        db.add_column(u'client_clientversion', 'current_installer',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ClientVersion.installer'
        db.delete_column(u'client_clientversion', 'installer')

        # Deleting field 'ClientVersion.current_installer'
        db.delete_column(u'client_clientversion', 'current_installer')


    models = {
        u'client.clientversion': {
            'Meta': {'object_name': 'ClientVersion'},
            'agent': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'current_agent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'current_installer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'current_updater': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'installer': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updater': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'})
        }
    }

    complete_apps = ['client']