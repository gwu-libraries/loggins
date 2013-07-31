"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils.timezone import utc

from datetime import datetime

from ui.models import Location, Session


class FloorURLTest(TestCase):

    def test_floor_url(self):
        location = Location()
        location.building = Location.GELMAN
        location.floor = 6
        location.station_name = 'PC601'
        location.hostname = 'FYWRXC3'
        location.ip_address = '192.168.1.111'
        location.os = Location.WINDOWS7
        location.state = Location.AVAILABLE
        location.save()

        response = self.client.get('/floor/' + Location.GELMAN +
                                   str(location.floor) + '/')
        self.assertEqual(response.context['locations'].count(), 1)


class SessionCreationTest(TestCase):

    def test_session_creation_signals(self):
        location = Location()
        location.building = Location.GELMAN
        location.floor = 6
        location.station_name = 'PC601'
        location.hostname = 'FYWRXC3'
        location.ip_address = '192.168.1.111'
        location.os = Location.WINDOWS7
        location.state = Location.AVAILABLE
        location.save()

        login_start_time = datetime.utcnow().replace(tzinfo=utc)
        location.observation_time = login_start_time
        location.state = Location.LOGGED_IN
        location.save()

        login_end_time = datetime.utcnow().replace(tzinfo=utc)
        location.observation_time = login_end_time
        location.state = Location.AVAILABLE
        location.save()

        #Test creation of login session
        login_session = Session.objects.get(location=location)
        self.assertEqual(login_session.session_type, Session.LOGIN)
        self.assertEqual(login_session.timestamp_start, login_start_time)
        self.assertEqual(login_session.timestamp_end, login_end_time)

        offline_start_time = datetime.utcnow().replace(tzinfo=utc)
        location.observation_time = offline_start_time
        location.state = Location.NO_RESPONSE
        location.save()

        offline_end_time = datetime.utcnow().replace(tzinfo=utc)
        location.observation_time = offline_end_time
        location.state = Location.AVAILABLE
        location.save()

        #Test creation of offline session
        offline_session = Session.objects.latest('id')
        self.assertEqual(offline_session.session_type, Session.OFFLINE)
        self.assertEqual(offline_session.timestamp_start, offline_start_time)
        self.assertEqual(offline_session.timestamp_end, offline_end_time)
