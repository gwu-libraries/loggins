from optparse import make_option

from django.core.management.base import BaseCommand
from django.db import connection

from ui.models import Record, Session, Anomaly


class Command(BaseCommand):
    help = 'create session and anomaly records based on logins'

    option_list = BaseCommand.option_list + (
            make_option('--empty', action='store_true', default=False,
                dest='empty', help='empty the sessions and anomalies tables'),
            )

    def handle(self, *args, **options):
        if options.get('empty', False):
            cursor = connection.cursor()
            print 'deleting %s sessions' % Session.objects.count()
            cursor.execute('DELETE FROM ui_session')
            cursor.execute('ALTER SEQUENCE ui_session_id_seq RESTART WITH 1')
            print 'deleting %s anomalies' % Anomaly.objects.count()
            cursor.execute('DELETE FROM ui_anomaly')
            cursor.execute('ALTER SEQUENCE ui_anomaly_id_seq RESTART WITH 1')
        records = Record.objects.order_by('timestamp')
        open_sessions = {}
        for record in records:
            if record.get_event_display() == 'login':
                # if there's a previous login open, it's an anomaly
                try:
                    open_session = open_sessions[record.host_id]
                    anomaly = Anomaly(login=open_session)
                    anomaly.save()
                    print 'A: %s (%s)' % (open_session.host_id, anomaly.id)
                except:
                    pass
                # either way, open the new session
                open_sessions[record.host_id] = record
            elif record.get_event_display() == 'logout':
                # an open session should exist; ignore when there isn't
                try:
                    open_session = open_sessions[record.host_id]
                    duration = record.timestamp - open_session.timestamp
                    duration_minutes = duration.seconds / 60
                    session = Session(host=record.host, 
                            login=open_session, logout=record,
                            timestamp_login=open_session.timestamp,
                            timestamp_logout=record.timestamp,
                            duration_minutes=duration_minutes)
                    session.save()
                    print 'S: %s (%s)' % (record.host_id, session.id)
                    del(open_sessions[record.host_id])
                except:
                    print 'LOLO: %s' % record.host_id
        print 'remaining open sessions:', open_sessions
