from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from ui.models import Location

from pysnmp.entity.rfc3413.oneliner import cmdgen


class Command(BaseCommand):
    help = '''Capture network status of all the hosts within the specified
            network and map hostname with ip address for registered locations'''
    args = '<network_prefix network_prefix...>'

    def handle(self, *args, **options):

        if len(args) < 1:
            raise CommandError("Please pass atleast one network prefix to " +
                               "perform the SNMP walk for mapping network " +
                               "hostnames with ip addresses.")

        cmdGen = cmdgen.CommandGenerator()
        for network_prefix in args:
            for i in range(256):
                ip_address = str(network_prefix) + '.' + str(i)

                try:
                    errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
                        cmdgen.CommunityData(settings.SNMP_COMMUNITY_STRING),
                        cmdgen.UdpTransportTarget((ip_address, 161)),
                        '1.3.6.1.4.1.25071.1.2.6.1.1.2',
                        '1.3.6.1.4.1.25071.1.1.2.1.1.3',)

                    if errorIndication:
                        print(str(ip_address) + ': ' + str(errorIndication))
                    else:
                        if errorStatus:
                            print('%s at %s' % (errorStatus.prettyPrint(),
                                                errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'))
                        else:
                            hostname = str(varBindTable[0][0][1])
                            try:
                                location = Location.objects.get(hostname__iexact=hostname)
                                if location.ip_address != ip_address:
                                    location.ip_address = ip_address
                                    location.save()
                                    print 'Updated IP address for host - %s' % location.hostname
                            except ObjectDoesNotExist:
                                print 'Location with hostname <' + hostname + '> does not exist.'
                except Exception as e:
                    print 'Error while querying - ' + ip_address
                    print 'Error message - %s' % str(e.message)
