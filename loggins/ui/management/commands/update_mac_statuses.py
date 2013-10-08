from django.core.management.base import BaseCommand

from ui.models import Location

import os


class Command(BaseCommand):
    help = 'Ping all the MAC-OSX machines registered in the system and update\
            their status if they are online/offline'

    def handle(self, *args, **options):
        hostnames = Location.objects.values('hostname')\
            .filter(os=Location.MACOSX)

        for hostname in hostnames:
            location = Location.objects.get(
                hostname__iexact=hostname['hostname'])

            try:
                response = os.system('ping -c 1 ' + location.ip_address)
                if response == 0:
                    if location.state != location.LOGGED_IN:
                        location.state = Location.AVAILABLE
                        print 'Location with hostname <' + location.hostname \
                            + '> and ip address <' + location.ip_address \
                            + '> is available'
                else:
                    location.state = Location.NO_RESPONSE
                    print 'Location with hostname <' + location.hostname \
                        + '> and ip address <' + location.ip_address \
                        + '> is offline'
            except Exception as e:
                print 'Error while pinging Location with hostname <' \
                    + location.hostname + '> and ip address <' \
                    + location.ip_address + '>: ' + str(e)

            location.save()
