# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


class Migration(DataMigration):

    def forwards(self, orm):
        # ---- POPULATE WITH NEW GWLIBRARY BUILDINGS, FLOORS, ZONES ----
        building_gelman = orm.Building(name='Gelman')
        building_gelman.save()
        building_eckles = orm.Building(name='Eckles')
        building_eckles.save()
        building_vstc = orm.Building(name='VSTC')
        building_vstc.save()

        floor_gelman0 = orm.Floor(floor=0, building=building_gelman)
        floor_gelman0.save()
        floor_gelman1 = orm.Floor(floor=1, building=building_gelman)
        floor_gelman1.save()
        floor_gelman2 = orm.Floor(floor=2, building=building_gelman)
        floor_gelman2.save()
        floor_gelman3 = orm.Floor(floor=3, building=building_gelman)
        floor_gelman3.save()
        floor_gelman4 = orm.Floor(floor=4, building=building_gelman)
        floor_gelman4.save()
        floor_gelman5 = orm.Floor(floor=5, building=building_gelman)
        floor_gelman5.save()
        floor_gelman6 = orm.Floor(floor=6, building=building_gelman)
        floor_gelman6.save()
        floor_gelman7 = orm.Floor(floor=7, building=building_gelman)
        floor_gelman7.save()
        floor_eckles1 = orm.Floor(floor=1, building=building_eckles)
        floor_eckles1.save()
        floor_eckles2 = orm.Floor(floor=2, building=building_eckles)
        floor_eckles2.save()
        floor_vstc1 = orm.Floor(floor=1, building=building_vstc)
        floor_vstc1.save()

        zone_gelmanll = orm.Zone(floor=floor_gelman0, name='Lower Level',
                                 display_order=0)
        zone_gelmanll.save()
        zone_gelman1 = orm.Zone(floor=floor_gelman1, name='1st Floor',
                                display_order=1)
        zone_gelman1.save()
        zone_gelmanentrance = orm.Zone(floor=floor_gelman2,
                                       name='Entrance Floor',
                                       display_order=2)
        zone_gelmanentrance.save()
        zone_gelmanlab = orm.Zone(floor=floor_gelman2,
                                  name='Lab @ Entrance Floor',
                                  display_order=3)
        zone_gelmanlab.save()
        zone_gelman3 = orm.Zone(floor=floor_gelman3, name='3rd Floor',
                                display_order=4)
        zone_gelman3.save()
        zone_gelman4 = orm.Zone(floor=floor_gelman4, name='4th Floor',
                                display_order=5)
        zone_gelman4.save()
        zone_gelman5 = orm.Zone(floor=floor_gelman5, name='5th Floor',
                                display_order=6)
        zone_gelman5.save()
        zone_gelman6 = orm.Zone(floor=floor_gelman6, name='6th Floor',
                                display_order=7)
        zone_gelman6.save()
        zone_gelman7 = orm.Zone(floor=floor_gelman7, name='7th Floor',
                                display_order=8)
        zone_gelman7.save()
        zone_gelmangrc = orm.Zone(floor=floor_gelman7,
                                  name='Global Resources Center',
                                  display_order=9)
        zone_gelmangrc.save()
        zone_gelmansc = orm.Zone(floor=floor_gelman7,
                                 name='Special Collections',
                                 display_order=10)
        zone_gelmansc.save()
        zone_eckles1 = orm.Zone(floor=floor_eckles1, name='Main',
                                display_order=0)
        zone_eckles1.save()
        zone_eckles2 = orm.Zone(floor=floor_eckles2, name='2nd Floor',
                                display_order=1)
        zone_eckles2.save()
        zone_vstc1 = orm.Zone(floor=floor_vstc1, name='Main',
                              display_order=0)
        zone_vstc1.save()

        # ---- MAP OLD LOCATION DATA TO NEW OBJECTS ----
        # try to find the entrance floor lab zone and
        # entrance floor non-lab zone
        labzone = orm.Zone.objects.get(floor__building__name='Gelman',
                                       floor__floor=2, name__contains="Lab")
        entrancemainzone = orm.Zone.objects.filter(
            floor__building__name='Gelman', floor__floor=2). \
            exclude(name__contains="Lab")[0]
        grczone = orm.Zone.objects.get(floor__building__name='Gelman',
                                       floor__floor=7, name__contains="Global")
        sczone = orm.Zone.objects.get(floor__building__name='Gelman',
                                      floor__floor=7, name__contains="Special")

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
            elif location.building == 'g' and '7-00' in location.station_name:
                zone = grczone
            elif location.building == 'g' and '7-01' in location.station_name:
                zone = sczone
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
