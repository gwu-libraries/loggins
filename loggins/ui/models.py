from django.contrib.auth.models import User
from django.contrib.humanize.templatetags import humanize
from django.db import models

from tastypie.models import create_api_key


models.signals.post_save.connect(create_api_key, sender=User)


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
    os = models.CharField(db_index=True, max_length=4, choices=OS_TYPES, default='', blank=True)

    def __unicode__(self):
        return '<Host %s %s>' % (self.location, self.name)

    def display_location(self):
        if len(self.location) != 4:
            return ''
        library_code = self.location[0]
        library = ''
        if library_code == 'g':
            library  = 'Gelman'
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
        super(Record, self).save(*args, **kwargs)


class Session(models.Model):
    host = models.ForeignKey(Host, related_name='sessions')
    login = models.ForeignKey(Record, related_name='session_login')
    logout = models.ForeignKey(Record, related_name='session_logout')
    timestamp_login = models.DateTimeField(db_index=True)
    timestamp_logout = models.DateTimeField(db_index=True)
    duration_minutes = models.IntegerField(db_index=True)

    @property
    def duration(self):
        return self.timestamp_logout - self.timestamp_login


class Anomaly(models.Model):
    login = models.ForeignKey(Record, related_name='anomalies')

