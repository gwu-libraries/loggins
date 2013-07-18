from optparse import make_option
import random
import time
from datetime import datetime

from django.utils.timezone import utc

from django.core.management.base import BaseCommand

from ui.models import Location

DEFAULT_NUM_MONKEYS = 5
DEFAULT_INTERVAL = 10

class Command(BaseCommand):
    help = 'test bot that generates random events'

    option_list = BaseCommand.option_list + (
        make_option('--interval', dest='interval', default=DEFAULT_INTERVAL,
                    help='seconds to wait before adding new events'),
        make_option('--monkeys', dest='monkeys', default=DEFAULT_NUM_MONKEYS,
                    help='number of monkey-locations to create'),
        make_option('--verbose', dest='verbose', default=False,
                    action='store_true', help='verbose output'),
    )

    def handle(self, *args, **options):
        if options['verbose']:
            print 'options:', options
        # initialize - make sure some monkey hosts exist
        # TODO: This will be updated later - for now, allow the monkeys to change
        # states of locations already in the database
        """
        for i in range(0, options.get('monkeys', 20)):
            l, created = Location.objects.get_or_create(station_name='monkey_%s' % i)
            if created:
                # put them in different buildings, on the first floor
                if i % 3 == 0:
                    h.location = 'g1%02d' % i
                elif i % 3 == 1:
                    h.location = 'e1%02d' % i
                elif i % 3 == 2:
                    h.location = 'v1%02d' % i
                h.save()
                if options['verbose']:
                    print 'host %s created' % h.name
            else:
                if options['verbose']:
                    print 'host %s exists' % h.name
        """

        while True:
            # we re-get locations each time, as locations may have changed
            locations = Location.objects.all()
            num_locations = locations.count()
            # for each monkey
            for i in range(0, int(options.get('monkeys', DEFAULT_NUM_MONKEYS))):
                # pick a random location
                location = Location.objects.get(id=random.randint(1, num_locations))
                randstate = random.randint(0, 2)
                if randstate == 0:
                    location.state = Location.AVAILABLE
                elif randstate == 1:
                    location.state = Location.LOGGED_IN
                elif randstate == 2:
                    location.state = Location.NO_RESPONSE
                location.observation_time = datetime.utcnow().replace(tzinfo=utc)
                location.save()
                print 'monkey #%d put location id=%d in state %s' % (i+1, location.id, location.state)
            time.sleep(float(options['interval']))

