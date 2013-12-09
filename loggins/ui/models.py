from django.contrib.auth.models import User
#from django.contrib.humanize.templatetags import humanize
from django.db import models
from django.db.models.signals import pre_save

from django.dispatch import receiver

from tastypie.models import create_api_key

models.signals.post_save.connect(create_api_key, sender=User)


class Building(models.Model):
    name = models.CharField(max_length=50, db_index=True)

    def __unicode__(self):
        return '<Building %s>' % (self.name)


class Floor(models.Model):
    floor = models.PositiveSmallIntegerField()
    building = models.ForeignKey(Building, related_name='buildings')

    def __unicode__(self):
        return '<Floor %d in %s>' % (self.floor, self.building.name)


class Zone(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    display_order = models.PositiveSmallIntegerField()
    floor = models.ForeignKey(Floor, related_name='floors')

    def __unicode__(self):
        return '<Zone %s in %s on floor %d>' % \
            (self.name, self.floor.building.name, self.floor.floor)


class Location(models.Model):
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

    zone = models.ForeignKey(Zone, related_name='zones', null=True)
    # station name/number does not have to be unique across floors/buildings
    station_name = models.CharField(max_length=50, db_index=True)
    hostname = models.CharField(max_length=50, db_index=True)
    ip_address = models.GenericIPAddressField(db_index=True, blank=True,
                                              null=True)
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
        return '<Location %s in %s>' % (self.station_name,
                                        self.zone.floor.building.name)

    """
    def display_floor(self):
        if self.floor == 0:
            return 'Lower Level'
        elif self.building == 'g' and self.floor == 2:
            return 'Entrance'
        else:
            return '%s' % humanize.ordinal(self.floor)
    """

    def building_name(self):
        return self.zone.floor.building.name

    def floor_number(self):
        return self.zone.floor.floor

    def zone_name(self):
        return self.zone.name


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

    #@property
    def duration(self):
        return self.timestamp_end - self.timestamp_start

    def duration_minutes(self):
        minutes = (self.timestamp_end -
                   self.timestamp_start).total_seconds()/60
        return round(minutes, 2)

    def session_type_display(self):
        return dict(Location.STATES)[self.session_type]


@receiver(pre_save, sender=Location)
def location_state_change_reciever(sender, instance, **kwargs):
    if instance.id:
        old_instance = Location.objects.get(id=instance.id)

        if old_instance.state == Location.AVAILABLE:
            if instance.state == Location.LOGGED_IN:
                print "User logged into %s" % instance
                instance.last_login_start_time = instance.observation_time

            elif instance.state == Location.NO_RESPONSE:
                print "%s went offline" % instance
                instance.last_offline_start_time = instance.observation_time

        elif old_instance.state == Location.LOGGED_IN:
            if instance.state != Location.LOGGED_IN:
                login_session = Session(session_type=Session.LOGIN)
                login_session.location = instance
                login_session.timestamp_start = instance.last_login_start_time
                login_session.timestamp_end = instance.observation_time
                login_session.save()

                print "Login session created for %s" % instance

                if instance.state == Location.NO_RESPONSE:
                    print "%s went offline" % instance
                    instance.last_offline_start_time = \
                        instance.observation_time

        elif old_instance.state == Location.NO_RESPONSE:
            if instance.state != Location.NO_RESPONSE:
                offline_session = Session(session_type=Session.OFFLINE)
                offline_session.location = instance
                offline_session.timestamp_start = \
                    instance.last_offline_start_time
                offline_session.timestamp_end = instance.observation_time
                offline_session.save()

                print "Offline session created for %s" % instance

                if instance.state == Location.LOGGED_IN:
                    print "User logged into %s" % instance
                    instance.last_login_start_time = instance.observation_time
