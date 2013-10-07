from datetime import datetime

from django.core.management.base import BaseCommand

from ui.models import Location

import subprocess


class Command(BaseCommand):
    help = 'Ping all the MAC-OSX machines registered in the system and update\
            their status if they are online/offline'

    def handle(self, *args, **options):

        hostnames = Location.objects.values('hostname').filter(os=Location.WINDOWS7)

        for hostname in hostnames:
            location = Location.objects.get(hostname__iexact=hostname['hostname'])

            process = subprocess.Popen('ping ' + str(location.ip_address), stdout=subprocess.PIPE)

            print 'Process return code: ' + process.returncode
            print 'Ping output: ' + process.stdout.read()
