# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table(u'ui_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('building', self.gf('django.db.models.fields.CharField')(default='', max_length=2, db_index=True)),
            ('floor', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('station_name', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('hostname', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('ip_address', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='', max_length=2, db_index=True)),
            ('observation_time', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('last_login_start_time', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('last_offline_start_time', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
        ))
        db.send_create_signal(u'ui', ['Location'])

        # Adding model 'Session'
        db.create_table(u'ui_session', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='locations', to=orm['ui.Location'])),
            ('timestamp_start', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('timestamp_end', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('session_type', self.gf('django.db.models.fields.CharField')(default='', max_length=2, db_index=True)),
        ))
        db.send_create_signal(u'ui', ['Session'])


    def backwards(self, orm):
        # Deleting model 'Location'
        db.delete_table(u'ui_location')

        # Deleting model 'Session'
        db.delete_table(u'ui_session')


    models = {
        u'ui.location': {
            'Meta': {'object_name': 'Location'},
            'building': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'db_index': 'True'}),
            'floor': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'last_login_start_time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'last_offline_start_time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'observation_time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'db_index': 'True'}),
            'station_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        u'ui.session': {
            'Meta': {'object_name': 'Session'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'locations'", 'to': u"orm['ui.Location']"}),
            'session_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'db_index': 'True'}),
            'timestamp_end': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'timestamp_start': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['ui']