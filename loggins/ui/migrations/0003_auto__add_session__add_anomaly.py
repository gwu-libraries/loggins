# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Session'
        db.create_table('ui_session', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('host', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sessions', to=orm['ui.Host'])),
            ('login', self.gf('django.db.models.fields.related.ForeignKey')(related_name='session_login', to=orm['ui.Record'])),
            ('logout', self.gf('django.db.models.fields.related.ForeignKey')(related_name='session_logout', to=orm['ui.Record'])),
            ('timestamp_login', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('timestamp_logout', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('duration_minutes', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
        ))
        db.send_create_signal('ui', ['Session'])

        # Adding model 'Anomaly'
        db.create_table('ui_anomaly', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('login', self.gf('django.db.models.fields.related.ForeignKey')(related_name='anomalies', to=orm['ui.Record'])),
        ))
        db.send_create_signal('ui', ['Anomaly'])


    def backwards(self, orm):
        # Deleting model 'Session'
        db.delete_table('ui_session')

        # Deleting model 'Anomaly'
        db.delete_table('ui_anomaly')


    models = {
        'ui.anomaly': {
            'Meta': {'object_name': 'Anomaly'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'anomalies'", 'to': "orm['ui.Record']"})
        },
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
        },
        'ui.session': {
            'Meta': {'object_name': 'Session'},
            'duration_minutes': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessions'", 'to': "orm['ui.Host']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'session_login'", 'to': "orm['ui.Record']"}),
            'logout': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'session_logout'", 'to': "orm['ui.Record']"}),
            'timestamp_login': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'timestamp_logout': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['ui']