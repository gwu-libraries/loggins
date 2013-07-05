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

#   is_active = models.BooleanField(default=True, db_index=True)
    building = models.CharField(db_index=True, max_length=2,
                                choices=BUILDINGS, default='')
    floor = models.PositiveSmallIntegerField()
    # station name/number may not be unique across floors/buildings
    station_name = models.CharField(max_length=50, db_index=True)
    hostname = models.CharField(max_length=50, db_index=True)
    ip_address = models.CharField(max_length=15, db_index=True)
    state = models.CharField(db_index=True, max_length=2,
                             choices=STATES, default='n')
    observation_time = models.DateTimeField(db_index=True, auto_now_add=True)
    last_login_start_time = models.DateTimeField(db_index=True,
                                                 auto_now_add=True)
    last_offline_start_time = models.DateTimeField(db_index=True,
                                                   auto_now_add=True)

    def __unicode__(self):
        return '<Station %s %s>' % (self.building, self.hostname)

    def display_floor(self):
        if self.floor == 0:
            return 'Lower Level'
        else:
            return '%s floor' % humanize.ordinal(self.floor)

"""
class Host(models.Model):

    WINDOWS7 = 'win7'
    MACOSX = 'mac'

    OS_TYPES = [
        (WINDOWS7, 'Windows 7'),
        (MACOSX, 'Mac OS-X'),
    ]

    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True, db_index=True)
    location = models.CharField(max_length=5, default='', db_index=True)
    os = models.CharField(db_index=True, max_length=4, choices=OS_TYPES,
                          default='', blank=True)

    def __unicode__(self):
        return '<Host %s %s>' % (self.location, self.name)

    def display_location(self):
        if len(self.location) != 4:
            return ''
        library_code = self.location[0]
        library = ''
        if library_code == 'g':
            library = 'Gelman'
        elif library_code == 'e':
            library = 'Eckles'
        elif library_code == 'v':
            library = 'VSTC'
        floor = self.location[1]
        return '%s %s floor' % (library, humanize.ordinal(floor))


class Record(models.Model):

    LOGIN = 'i'
    LOGOUT = 'o'
    MAINTENANCE = 'm'
    AVAILABLE = 'a'
    EVENT_TYPES = [
        (LOGIN, 'login'),
        (LOGOUT, 'logout'),
        (MAINTENANCE, 'maintenance'),
        (AVAILABLE, 'available'),
    ]

    host = models.ForeignKey(Host, related_name='records')
    hostname = models.CharField(max_length=50, db_index=True)
    event = models.CharField(db_index=True, max_length=2,
                             choices=EVENT_TYPES, default=LOGIN)
    timestamp = models.DateTimeField(db_index=True, auto_now_add=True)

    def __unicode__(self):
        return '<Record %s %s (%s)>' % (self.host.location,
                                        self.get_event_display(), self.id)

    def save(self, *args, **kwargs):
        host, created = Host.objects.get_or_create(name=self.hostname)
        self.host = host
        super(Record, self).save(*args, **kwargs) """


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
