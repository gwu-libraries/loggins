from datetime import datetime

from django.utils.timezone import utc
from django.core.management.base import BaseCommand
from django.conf import settings

from ui.models import Location

from pysnmp.entity.rfc3413.oneliner import cmdgen


class Command(BaseCommand):
    help = 'Record current SNMP state of all the machines registered in the system'

    def handle(self, *args, **options):
        cmdGen = cmdgen.CommandGenerator()

        hostnames = Location.objects.values('hostname')

        for hostname in hostnames:
            location = Location.objects.get(hostname__iexact=hostname['hostname'])
            errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
                cmdgen.CommunityData(settings.SNMP_COMMUNITY_STRING), cmdgen.UdpTransportTarget(
                    (location.ip_address, 161)),
                '1.3.6.1.4.1.25071.1.2.6.1.1.2',
                '1.3.6.1.4.1.25071.1.1.2.1.1.3',)
            location.observation_time = datetime.utcnow().replace(tzinfo=utc)

            if errorIndication:
                print(str(location.ip_address) + ': ' + str(errorIndication))
                location.state = Location.NO_RESPONSE
            else:
                if errorStatus:
                    print('%s at %s' % (errorStatus.prettyPrint(),
                                        errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'))
                    location.state = Location.NO_RESPONSE
                else:
                    hostname = varBindTable[0][0][1]
                    status = varBindTable[0][1][1]
                    if status == 0:
                        location.state = Location.AVAILABLE
                        print '%s - %s' % (hostname, Location.STATES[0][1])
                    else:
                        location.state = Location.LOGGED_IN
                        print '%s - %s' % (hostname, Location.STATES[1][1])
            location.save()
