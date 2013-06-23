# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ClientVersion'
        db.create_table(u'client_clientversion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('agent', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True)),
            ('updater', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True)),
            ('current_agent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('current_updater', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'client', ['ClientVersion'])


    def backwards(self, orm):
        # Deleting model 'ClientVersion'
        db.delete_table(u'client_clientversion')


    models = {
        u'client.clientversion': {
            'Meta': {'object_name': 'ClientVersion'},
            'agent': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'current_agent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'current_updater': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updater': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'})
        }
    }

    complete_apps = ['client']