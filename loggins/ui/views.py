from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection
from django.shortcuts import get_object_or_404, render

from ui.models import Host, Record


def _paginate(request, paginator):
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return page, items


def home(request):
    cursor = connection.cursor()
    cursor.execute('''
        SELECT COUNT(*), 
            SUBSTRING(ui_host.location FROM 1 FOR 1) AS library, 
            SUBSTRING(ui_host.location FROM 2 FOR 1) AS floor, event
            FROM ui_record r1, ui_host        
            WHERE timestamp=(
                SELECT MAX(timestamp)
                FROM ui_record
                WHERE host_id=r1.host_id
                AND location != ''
            )
            AND ui_host.id = r1.host_id
            AND ui_host.is_active IS true 
            GROUP BY library, floor, event 
            ORDER BY library, floor, event;
        ''')
    codes = {}
    # presuming a small dataset; we can get away with fetchall()
    for row in cursor.fetchall():
        count, library, floor, event = row        
        code = library + floor
        try:
            s = codes[code]
        except:
            s = {'code': code, 'floor': floor}
        if library == 'g':
            s['library'] = 'Gelman'
        elif library == 'e':
            s['library'] = 'Eckles'
        elif library == 'v':
            s['library'] = 'VSTC'
        if event == 'i':
            s['unavailable'] = count
        elif event == 'o':
            s['available'] = count
        s['total'] = s.get('available', 0) + s.get('unavailable', 0)
        codes[code] = s
    all_floors = sorted([(code, s) for code, s in codes.items()])
    floors = [floor for code, floor in all_floors]
    cursor.execute('''
        SELECT host_id, location, COUNT(*) AS the_count 
        FROM ui_session, ui_host 
        WHERE ui_host.id = ui_session.host_id 
        AND ui_host.is_active = True 
        GROUP BY host_id, location
        ORDER BY the_count DESC; 
        ''')
    host_counts = [{'host_id': row[0], 'location': row[1], 'count': row[2]}
            for row in cursor.fetchall()]
    return render(request, 'home.html', {
        'title': 'home',
        'codes': codes,
        'floors': floors,
        'host_counts': host_counts,
    })


def host(request, host_location):
    host = get_object_or_404(Host, location=host_location, is_active=True)
    paginator = Paginator(host.sessions.order_by('-timestamp_login'), 25)
    page, sessions = _paginate(request, paginator)
    return render(request, 'host.html', {
        'title': 'host: %s (%s)' % (host.id, host.location),
        'host': host,
        'sessions': sessions,
        'paginator': paginator,
        'page': page,
    })


def floor(request, code):
    hosts = Record.objects.raw('''
        SELECT *
        FROM ui_record r1, ui_host        
        WHERE timestamp=(
            SELECT MAX(timestamp)
            FROM ui_record
            WHERE host_id=r1.host_id
            AND SUBSTRING(location FROM 1 FOR 2) = %s
        )
        AND ui_host.id = r1.host_id
        AND ui_host.is_active IS true
        ORDER BY location
        ''', [code])
    return render(request, 'floor.html', {
        'title': 'floor: %s' % code,
        'hosts': hosts,
    })
