# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Zone'
        db.create_table(u'ui_zone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('display_order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('floor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='floors', to=orm['ui.Floor'])),
        ))
        db.send_create_signal(u'ui', ['Zone'])

        # Adding model 'Floor'
        db.create_table(u'ui_floor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('floor', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('building', self.gf('django.db.models.fields.related.ForeignKey')(related_name='buildings', to=orm['ui.Building'])),
        ))
        db.send_create_signal(u'ui', ['Floor'])

        # Adding model 'Building'
        db.create_table(u'ui_building', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal(u'ui', ['Building'])

        # Adding field 'Location.zone'
        db.add_column(u'ui_location', 'zone',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='zones', null=True, to=orm['ui.Zone']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Zone'
        db.delete_table(u'ui_zone')

        # Deleting model 'Floor'
        db.delete_table(u'ui_floor')

        # Deleting model 'Building'
        db.delete_table(u'ui_building')

        # Deleting field 'Location.zone'
        db.delete_column(u'ui_location', 'zone_id')


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
            'building': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'db_index': 'True'}),
            'floor': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
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