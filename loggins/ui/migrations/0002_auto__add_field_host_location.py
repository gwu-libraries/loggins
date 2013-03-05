# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Host.location'
        db.add_column('ui_host', 'location',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=5, db_index=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Host.location'
        db.delete_column('ui_host', 'location')


    models = {
        'ui.host': {
            'Meta': {'object_name': 'Host'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'ui.record': {
            'Meta': {'object_name': 'Record'},
            'event': ('django.db.models.fields.CharField', [], {'default': "'i'", 'max_length': '2', 'db_index': 'True'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'records'", 'to': "orm['ui.Host']"}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['ui']