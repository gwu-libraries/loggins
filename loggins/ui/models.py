from django.contrib.auth.models import User
from django.db import models

from tastypie.models import create_api_key


models.signals.post_save.connect(create_api_key, sender=User)


class Host(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True, db_index=True)

    def __unicode__(self):
        return '%s' % self.name


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

    def save(self, *args, **kwargs):
        host, created = Host.objects.get_or_create(name=self.hostname)
        self.host = host
        super(Record, self).save(*args, **kwargs)
