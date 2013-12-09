# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        user_verify = raw_input("*** WARNING *** This migration is irreverisble! Have you backed up your database (Y/N)? ")
        if user_verify.lower() != 'y' and user_verify.lower() != 'yes':
            print "Aborting. Please back up your database before running this migration."
            raise RuntimeError("Cannot proceed until user indicates that database has been backed up.")

        # Deleting field 'Location.building'
        db.delete_column(u'ui_location', 'building')

        # Deleting field 'Location.floor'
        db.delete_column(u'ui_location', 'floor')


    def backwards(self, orm):
        # Adding field 'Location.building'
        db.add_column(u'ui_location', 'building',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=2, db_index=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Location.floor'
        raise RuntimeError("Cannot reverse this migration. 'Location.floor' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Location.floor'
        db.add_column(u'ui_location', 'floor',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(),
                      keep_default=False)


    models = {
        u'ui.building': {
            'Meta': {'object_name': 'Building'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        u'ui.floor': {
            'Meta': {'object_name': 'Floor'},
            'building': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'buildings'", 'to': u"orm['ui.Building']"}),
            'floor': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'ui.location': {
            'Meta': {'object_name': 'Location'},
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.GenericIPAddressField', [], {'db_index': 'True', 'max_length': '39', 'null': 'True', 'blank': 'True'}),
            'last_login_start_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'last_offline_start_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'observation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'os': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'db_index': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'n'", 'max_length': '2', 'db_index': 'True'}),
            'station_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'zones'", 'null': 'True', 'to': u"orm['ui.Zone']"})
        },
        u'ui.session': {
            'Meta': {'object_name': 'Session'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'locations'", 'to': u"orm['ui.Location']"}),
            'session_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'db_index': 'True'}),
            'timestamp_end': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'timestamp_start': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        u'ui.zone': {
            'Meta': {'object_name': 'Zone'},
            'display_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'floor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'floors'", 'to': u"orm['ui.Floor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['ui']
