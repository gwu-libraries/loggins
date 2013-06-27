# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Host.os'
        db.add_column(u'ui_host', 'os',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=4, db_index=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Host.os'
        db.delete_column(u'ui_host', 'os')


    models = {
        u'ui.anomaly': {
            'Meta': {'object_name': 'Anomaly'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'anomalies'", 'to': u"orm['ui.Record']"})
        },
        u'ui.host': {
            'Meta': {'object_name': 'Host'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'os': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'db_index': 'True'})
        },
        u'ui.record': {
            'Meta': {'object_name': 'Record'},
            'event': ('django.db.models.fields.CharField', [], {'default': "'i'", 'max_length': '2', 'db_index': 'True'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'records'", 'to': u"orm['ui.Host']"}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'})
        },
        u'ui.session': {
            'Meta': {'object_name': 'Session'},
            'duration_minutes': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessions'", 'to': u"orm['ui.Host']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'session_login'", 'to': u"orm['ui.Record']"}),
            'logout': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'session_logout'", 'to': u"orm['ui.Record']"}),
            'timestamp_login': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'timestamp_logout': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['ui']