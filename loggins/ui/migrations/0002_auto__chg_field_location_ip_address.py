# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Location.ip_address'
        db.alter_column(u'ui_location', 'ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Location.ip_address'
        raise RuntimeError("Cannot reverse this migration. 'Location.ip_address' and its values cannot be restored.")

    models = {
        u'ui.location': {
            'Meta': {'object_name': 'Location'},
            'building': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'db_index': 'True'}),
            'floor': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'last_login_start_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'last_offline_start_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'observation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'os': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'db_index': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'n'", 'max_length': '2', 'db_index': 'True'}),
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