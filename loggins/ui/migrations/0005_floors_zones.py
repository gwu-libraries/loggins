# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


class Migration(DataMigration):

    def forwards(self, orm):
        # try to find the entrance floor lab zone and
        # entrance floor non-lab zone
        labzone = orm.Zone.objects.get(floor__building__name='Gelman',
                                       floor__floor=2, name__contains="Lab")
        entrancemainzone = orm.Zone.objects.filter(
            floor__building__name='Gelman', floor__floor=2). \
            exclude(name__contains="Lab")[0]

        # for each location, find the (first) matching zone
        # by building and floor number.
        for location in orm.Location.objects.all():
            buildingname = {'g': 'Gelman', 'e': 'Eckles',
                            'v': 'VSTC'}[location.building]
            # special case for Gelman Entrance Floor
            if location.building == 'g' and 'E-' in location.station_name:
                if 'E-L' in location.station_name:
                    zone = labzone
                else:
                    zone = entrancemainzone
            # all others
            else:
                try:
                    zone = orm.Zone.objects.filter(
                        floor__building__name=buildingname,
                        floor__floor=location.floor)[0]
                except Exception:
                    print("%s --  NO ZONE MATCHED; stopping." %
                          location.station_name)
                    raise

            print("%s --  zone = %s %s %s" % (location.station_name,
                                              zone.name,
                                              zone.floor.building.name,
                                              zone.floor.floor))
            location.zone = zone
            location.save()

    def backwards(self, orm):
        "Write your backwards methods here."

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
    symmetrical = True
