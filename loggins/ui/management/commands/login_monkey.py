from optparse import make_option
import random
import time

from django.core.management.base import BaseCommand

from ui.models import Host, Record


class Command(BaseCommand):
    help = 'test bot that generates random events'

    option_list = BaseCommand.option_list + (
        make_option('--interval', dest='interval', default=10,
                    help='seconds to wait before adding new events'),
        make_option('--monkeys', dest='monkeys', default=20,
                    help='number of monkey-hosts to create'),
        make_option('--verbose', dest='verbose', default=False,
                    action='store_true', help='verbose output'),
    )

    def handle(self, *args, **options):
        if options['verbose']:
            print 'options:', options
        # initialize - make sure some monkey hosts exist
        for i in range(0, options.get('monkeys', 20)):
            h, created = Host.objects.get_or_create(name='monkey_%s' % i)
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
        while True:
            # subtract one off the end to avoid off-by-one error w/max
            monkey_num = random.randint(0, options.get('monkeys', 20) - 1)
            host = Host.objects.get(name='monkey_%s' % monkey_num)
            qs_latest_record = Record.objects.filter(host=host)
            qs_latest_record = qs_latest_record.order_by('-timestamp')
            new_record = Record(host=host, hostname=host.name)
            if qs_latest_record.count() == 0:
                new_record.event = Record.LOGIN
            else:
                latest_record = qs_latest_record[0]
                if latest_record.event == Record.LOGIN:
                    new_record.event = Record.LOGOUT
                elif latest_record.event == Record.LOGOUT:
                    new_record.event = Record.LOGIN
            new_record.save()
            print 'saved new_record:', new_record
            time.sleep(float(options['interval']))
