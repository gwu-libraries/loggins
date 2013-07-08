from django.contrib.auth.models import User
from django.contrib.humanize.templatetags import humanize
from django.db import models

from tastypie.models import create_api_key

models.signals.post_save.connect(create_api_key, sender=User)


class Location(models.Model):
    GELMAN = 'g'
    ECKLES = 'e'
    VSTC = 'v'
    BUILDINGS = [
        (GELMAN, 'Gelman'),
        (ECKLES, 'Eckles'),
        (VSTC, 'VSTC'),
    ]

    AVAILABLE = 'a'
    LOGGED_IN = 'i'
    NO_RESPONSE = 'n'
    STATES = [
        (AVAILABLE, 'available'),
        (LOGGED_IN, 'in use'),
        (NO_RESPONSE, 'offline'),
    ]

    WINDOWS7 = 'win7'
    MACOSX = 'mac'
    OS_TYPES = [
        (WINDOWS7, 'Windows 7'),
        (MACOSX, 'Mac OS-X'),
    ]

    building = models.CharField(db_index=True, max_length=2,
                                choices=BUILDINGS, default='')
    floor = models.PositiveSmallIntegerField()
    # station name/number may not be unique across floors/buildings
    station_name = models.CharField(max_length=50, db_index=True)
    hostname = models.CharField(max_length=50, db_index=True)
    ip_address = models.IPAddressField(db_index=True)
    os = models.CharField(db_index=True, max_length=4, choices=OS_TYPES,
                          default='', blank=True)
    state = models.CharField(db_index=True, max_length=2,
                             choices=STATES, default='n')
    observation_time = models.DateTimeField(db_index=True, auto_now_add=True)
    last_login_start_time = models.DateTimeField(db_index=True,
                                                 auto_now_add=True)
    last_offline_start_time = models.DateTimeField(db_index=True,
                                                   auto_now_add=True)

    def __unicode__(self):
        return '<Station %s %s %s>' % (self.building, self.floor,
                                       self.station_name)

    def display_floor(self):
        if self.floor == 0:
            return 'Lower Level'
        else:
            return '%s floor' % humanize.ordinal(self.floor)


class Session(models.Model):
    LOGIN = 'i'
    OFFLINE = 'n'
    SESSION_TYPES = [
        (LOGIN, 'login'),
        (OFFLINE, 'offline'),
    ]
    location = models.ForeignKey(Location, related_name='locations')
    timestamp_start = models.DateTimeField(db_index=True)
    timestamp_end = models.DateTimeField(db_index=True)
    session_type = models.CharField(db_index=True, max_length=2,
                                    choices=SESSION_TYPES, default='')

    @property
    def duration(self):
        return self.timestamp_end - self.timestamp_start


#class Anomaly(models.Model):
#    login = models.ForeignKey(Record, related_name='anomalies')
